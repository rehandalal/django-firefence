# django-firefence

[![PyPI](https://img.shields.io/pypi/v/django-firefence.svg)](https://pypi.python.org/pypi/django-firefence) [![Travis](https://img.shields.io/travis/rehandalal/django-firefence.svg)](https://travis-ci.org/rehandalal/django-firefence) [![Codecov](https://img.shields.io/codecov/c/github/rehandalal/django-firefence.svg)](https://codecov.io/gh/rehandalal/django-firefence)
 
![Django 1.9](https://img.shields.io/badge/Django-1.8-orange.svg) ![Django 1.9](https://img.shields.io/badge/Django-1.9-orange.svg) ![Django 1.10](https://img.shields.io/badge/Django-1.10-orange.svg) ![Django 1.11](https://img.shields.io/badge/Django-1.11-orange.svg)

### Quick Start

Install from PyPI:

```
pip install django-firefence
```

Add the middleware and configure some rules:

```python
MIDDLEWARE = [
    ...

    'firefence.middleware.FirefenceMiddleware',
    ...
]

FIREFENCE = {
    'RULES': [
        {
            'action': 'ALLOW',
            'host': '192.168.1.1',
            'port': '80, 443',
        }
    ]
}
```

This will check all incoming requests to your app against these rules. Use of the middleware is
optional and you can check only certain views by using provided decorators. Please consult the 
[documentation](http://django-firefence.readthedocs.io/) for more information.

### About

django-firefence is a project developed to provide firewall style request filtering to a Django
project at the application level or at the view level.

The library is compatible with currently supported versions of Django.

### Found a bug? Looking for a new feature?

Feel free to file an issue on the 
[Github project issue page](https://github.com/rehandalal/django-firefence/issues).

### Documentation

Full documentation is available at: 
http://django-firefence.readthedocs.io/
