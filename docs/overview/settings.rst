Settings
========

All the settings are optional and can be set in your Django settings file as follows:

    .. code-block:: python

        FIREFENCE = {
            'RULES': [
                {
                    'action': 'ALLOW',
                    'host': '192.168.1.1',
                    'port': '80, 443',
                }
            ],
            'DEFAULT_BACKEND': 'firefence.backends.Fence',
        }


RULES (default: ``()``)
    A list or tuple of default rules. These will be used by the middleware or the decorator (if
    not specified).

    Rules may be ``dict``s or ``Rule`` objects.


DEFAULT_BACKEND (default: ``'firefence.backends.Fence'``)
    An import path for the backend class to use. This backend will be used by the middleware and
    the decorator (if not specified).
