from firefence.backends import get_backend_class
from firefence.settings import FIREFENCE_SETTINGS


def fence_protected(rules=None, backend_class=None):
    backend_class = backend_class or get_backend_class()
    rules = rules or FIREFENCE_SETTINGS.get('RULES')
    fence = backend_class(rules)
    return fence.protect
