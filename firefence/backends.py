from functools import wraps

import ipcalc

from django.core.exceptions import PermissionDenied

from firefence.exceptions import InvalidRule


def get_client_ip(request):
    xff = request.META.get('HTTP_X_FORWARDED_FOR')
    return xff.split(',').pop() if xff else request.META.get('REMOTE_ADDR')


def get_server_port(request):
    return request.META.get('HTTP_X_FORWARDED_PORT', request.META.get('SERVER_PORT'))


class Rule(object):
    def __init__(self, type, ips=(), ports=()):
        if type not in ('allow', 'deny'):
            raise InvalidRule('Rule type must be ALLOW or DENY.')

        self.type = type.lower()
        self.ips = ips
        self.ports = [str(port) for port in ports]

    def ip_allowed(self, request):
        ip = get_client_ip(request)

        if self.ips:
            ip_matched = False

            for rule_ip in self.ips:
                ip_matched |= ip in ipcalc.Network(rule_ip)

            if (self.type == 'allow' and not ip_matched) or (self.type == 'deny' and ip_matched):
                return False

        return True

    def port_allowed(self, request):
        port = get_server_port(request)
        return port in self.ports if self.ports else True

    def allowed(self, request):
        return self.ip_allowed(request) and self.port_allowed(request)


class Fence(object):
    def __init__(self, rules=None):
        self.rules = rules

    def allowed(self, request):
        if self.rules:
            allowed = False

            for rule in self.rules:
                if 'type' not in rule:
                    raise InvalidRule('Rules must have a type.')

                allowed |= Rule(**rule).allowed(request)

            return allowed
        return True

    def reject(self):
        raise PermissionDenied()

    def protect(self):
        def decorator(view_func):
            @wraps(view_func)
            def wrapped_view(request, *args, **kwargs):
                if not self.allowed(request):
                    return self.reject()
                return view_func(request, *args, **kwargs)
            return wrapped_view
        return decorator
