from django.test.client import RequestFactory

from firefence.backends import AbstractFence


def mock_request(**kwargs):
    """Creates a request object for testing."""
    rf = RequestFactory()
    return rf.get('/', **kwargs)


class CustomFence(AbstractFence):
    """A custom backend for testing purposes."""
    class Rejection(Exception):
        pass

    def reject(self, request, *args, **kwargs):
        raise self.Rejection()
