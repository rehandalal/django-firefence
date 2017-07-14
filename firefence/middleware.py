from django.conf import settings
from django.utils.module_loading import import_string

from firefence import Fence


class FirefenceMiddleware(object):
    def __init__(self, get_response=None):
        self.get_response = get_response
        super(FirefenceMiddleware, self).__init__()

    def __call__(self, request):
        return self.process_request(request)

    def process_request(self, request):
        default_backend = getattr(settings, 'FIREFENCE_DEFAULT_BACKEND', Fence)
        if isinstance(default_backend, str):
            default_backend = import_string(default_backend)

        fence = default_backend(getattr(settings, 'FIREFENCE_RULES'))

        if not fence.allowed(request):
            fence.reject()
