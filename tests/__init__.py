from django.test.client import RequestFactory

from firefence.backends import AbstractFence


def mock_request(**kwargs):
    """Creates a request object for testing."""
    rf = RequestFactory(**kwargs)
    return rf.get('/')


class CustomFence(AbstractFence):
    """A custom backend for testing purposes."""
    class Rejection(Exception):
        pass

    def reject(self):
        raise self.Rejection()
