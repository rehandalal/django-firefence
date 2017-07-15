from django.conf import settings


FIREFENCE_SETTINGS = {
    'DEFAULT_BACKEND': 'firefence.backends.Fence',
    'RULES': (),
}

if hasattr(settings, 'FIREFENCE'):
    FIREFENCE_SETTINGS.update(settings.FIREFENCE)
