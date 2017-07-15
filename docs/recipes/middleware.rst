Middleware
==========

The easiest, but least flexible way to use django-firence is to simply install the
``FirefenceMiddleware`` middleware and define some default rules:

    .. code-block:: python

        MIDDLEWARE += ['firefence.middleware.FirefenceMiddleware']

        FIREFENCE= {
            'RULES': [
                {
                    'action': 'ALLOW',
                    'host': '192.168.1.1',
                    'port': '80, 443',
                }
            ],
        }

When using the middleware, *ALL* requests are filtered through the default rules.

By default the middleware uses the provided ``Fence`` backend, however you may change the
``DEFAULT_BACKEND`` setting to use a custom backend.
