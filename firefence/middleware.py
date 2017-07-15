from firefence.backends import get_backend_class
from firefence.settings import FIREFENCE_SETTINGS


class FirefenceMiddleware(object):
    def __init__(self, get_response=None):
        self.get_response = get_response
        super(FirefenceMiddleware, self).__init__()

    def __call__(self, request):
        response = self.process_request(request)
        if not response:
            response = self.get_response(request)
        return response

    def process_request(self, request):
        backend_class = get_backend_class()
        fence = backend_class(FIREFENCE_SETTINGS.get('RULES'))
        if not fence.allows(request):
            return fence.reject(request)
