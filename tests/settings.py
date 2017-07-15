SECRET_KEY = '^$=xuqi0n!bjc)19%9tz$$0phu3$8i-whx$q^d6xq*rng0s^$o'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }
}

FIREFENCE = {
    'DEFAULT_BACKEND': 'tests.CustomFence',
    'RULES': [{
        'action': 'ALLOW',
        'address': '192.168.1.1',
    }],
}
