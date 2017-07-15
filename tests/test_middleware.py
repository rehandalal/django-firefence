import pytest

from django.test import TestCase

from mock import Mock

from firefence.middleware import FirefenceMiddleware

from . import CustomFence, mock_request


class TestFirefenceMiddleware(TestCase):
    def test_it_works(self):
        """Test that the middleware works as expected."""
        middleware = FirefenceMiddleware(Mock())

        # Ensure no errors when connecting from an allowed address
        middleware(mock_request(REMOTE_ADDR='192.168.1.1'))

        # Exception is raised when connection from a banned address
        with pytest.raises(CustomFence.Rejection):
            middleware(mock_request(REMOTE_ADDR='127.0.0.1'))
