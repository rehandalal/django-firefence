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

These are the available settings:

:RULES: A list or tuple of default rules. These will be used by the middleware or the decorator
        (if not specified).

        **DEFAULT:** ``()``


:DEFAULT_BACKEND: An import path for the backend class to use. This backend will be used by the
                  middleware and the decorator (if not specified).

                  **DEFAULT:** ``'firefence.backends.Fence'``
