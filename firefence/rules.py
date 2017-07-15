import ipcalc


def get_remote_ip(request):
    xff = request.META.get('HTTP_X_FORWARDED_FOR')
    return xff.split(',')[0] if xff else request.META.get('REMOTE_ADDR')


def get_remote_host(request):
    return request.META.get('HTTP_X_FORWARDED_HOST', request.META.get('REMOTE_HOST'))


def get_server_port(request):
    try:
        return int(request.META.get('HTTP_X_FORWARDED_PORT', request.META.get('SERVER_PORT')))
    except (TypeError, ValueError):
        return None


class Rule(object):
    ALLOW = 'ALLOW'
    DENY = 'DENY'

    _action = None
    _ports = ()
    host = None

    def __init__(self, **kwargs):
        if 'action' not in kwargs:
            raise ValueError('Rules must have an action.')
        self.action = kwargs.get('action')
        self.host = kwargs.get('host')
        self.port = kwargs.get('port')

    def __str__(self):
        string = self.action
        if self.host:
            string += ' from {}'.format(self.host)
        if self.port:
            string += ' to {}'.format(self.port)
        return string or ''

    def __repr__(self):
        return '<Rule: {}>'.format(self)

    @property
    def action(self):
        return self._action

    @action.setter
    def action(self, value):
        if value.upper() not in (self.ALLOW, self.DENY):
            raise ValueError('Action must be ALLOW or DENY.')
        self._action = value.upper()

    @property
    def port(self):
        if self._ports:
            if len(self._ports) == 1:
                return str(self._ports[0])
            else:
                if set(self._ports) == set(range(self._ports[0], self._ports[-1] + 1)):
                    return '{}:{}'.format(self._ports[0], self._ports[-1])
                else:
                    return ', '.join([str(port) for port in self._ports])
        return None

    @port.setter
    def port(self, value):
        if value is None:
            self._ports = ()
        elif isinstance(value, (str, int)):
            ports = str(value).split(',')
            if len(ports) == 1:
                ports = ports[0].split(':', 1)

                if len(ports) == 1:
                    self._ports = (int(ports[0]),)
                else:
                    self._ports = tuple(range(int(ports[0]), int(ports[1]) + 1))
            else:
                self._ports = tuple(sorted([int(port) for port in set(ports)]))
        elif isinstance(value, (list, tuple)):
            self._ports = tuple([int(port) for port in value])
        else:
            raise TypeError(
                'Port must be a string or integer or a list or tuple of strings or integers.')

    def host_matches(self, request):
        remote_ip = get_remote_ip(request)
        remote_host = get_remote_host(request)

        if self.host:
            if remote_host == self.host:
                return True

            try:
                return remote_ip in ipcalc.Network(self.host)
            except ValueError:
                return False

        return True

    def port_matches(self, request):
        server_port = get_server_port(request)
        return server_port in self._ports if self.port else True

    def matches(self, request):
        return self.host_matches(request) and self.port_matches(request)


class RuleSet(object):
    _rules = ()

    def __init__(self, rules=None):
        self.rules = rules

    def __len__(self):
        return len(self.rules)

    def __getitem__(self, index):
        return self.rules[index]

    def __iter__(self):
        return self.rules.__iter__()

    def __str__(self):
        return '\n'.join([str(rule) for rule in self.rules])

    def __repr__(self):
        return repr(self.rules)

    @property
    def rules(self):
        return self._rules

    @rules.setter
    def rules(self, value):
        if value is None:
            self._rules = ()
        else:
            if not isinstance(value, (list, tuple)):
                raise TypeError('Expected a list or tuple of rules.')

            rules = []
            for rule in value:
                if isinstance(rule, Rule):
                    rules.append(rule)
                elif isinstance(rule, dict):
                    rules.append(Rule(**rule))
                else:
                    raise TypeError('Expected a Rule or dict.')
            self._rules = tuple(rules)

    def allows(self, request):
        default = True

        for rule in self.rules:
            if rule.action == Rule.DENY and rule.matches(request):
                return False
            elif rule.action == Rule.ALLOW:
                # Change the default if an ALLOW rule exists
                default = False

                if rule.matches(request):
                    return True

        return default
