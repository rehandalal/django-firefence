from functools import wraps

from django.core.exceptions import PermissionDenied
from django.utils.module_loading import import_string

from firefence.rules import RuleSet
from firefence.settings import FIREFENCE_SETTINGS


def get_backend_class(import_path=None):
    return import_string(import_path or FIREFENCE_SETTINGS.get('DEFAULT_BACKEND'))


class AbstractFence(object):
    _rules = RuleSet()

    def __init__(self, rules=None):
        self.rules = rules

    @property
    def rules(self):
        return self._rules

    @rules.setter
    def rules(self, value):
        if isinstance(value, RuleSet):
            self._rules = value
        else:
            self._rules = RuleSet(value)

    def allows(self, request):
        return self.rules.allows(request)

    def reject(self, request, *args, **kwargs):
        raise NotImplementedError()  # pragma: no cover

    def protect(self, view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            if not self.allows(request):
                return self.reject(request, *args, **kwargs)
            return view_func(request, *args, **kwargs)
        return wrapped_view


class Fence(AbstractFence):
    def reject(self, request, *args, **kwargs):
        raise PermissionDenied
