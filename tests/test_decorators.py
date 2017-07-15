import pytest

from django.core.exceptions import PermissionDenied
from django.test import TestCase

from firefence.backends import Fence
from firefence.decorators import fence_protected
from firefence.rules import Rule

from . import CustomFence, mock_request


@fence_protected()
def default_view(request):
    return True


@fence_protected(rules=[Rule(action=Rule.ALLOW, host='127.0.0.1')])
def rules_view(request):
    return True


@fence_protected(backend_class=Fence)
def backend_view(request):
    return True


@fence_protected(rules=[Rule(action=Rule.ALLOW, host='127.0.0.1')], backend_class=Fence)
def custom_view(request):
    return True


class TestFenceProtected(TestCase):
    def test_default_rules_default_backend(self):
        """Test the decorator with all defaults."""
        assert default_view(mock_request(REMOTE_ADDR='192.168.1.1'))

        with pytest.raises(CustomFence.Rejection):
            default_view(mock_request(REMOTE_ADDR='127.0.0.1'))

    def test_custom_rules_default_backend(self):
        """Test the decorator with custom rules."""
        with pytest.raises(CustomFence.Rejection):
            assert rules_view(mock_request(REMOTE_ADDR='192.168.1.1'))

        assert rules_view(mock_request(REMOTE_ADDR='127.0.0.1'))

    def test_default_rules_custom_backend(self):
        """Test the decorator with a custom backend."""
        assert backend_view(mock_request(REMOTE_ADDR='192.168.1.1'))

        with pytest.raises(PermissionDenied):
            assert backend_view(mock_request(REMOTE_ADDR='127.0.0.1'))

    def test_custom_rules_custom_backend(self):
        """Test decorator with custom rules and backend."""
        with pytest.raises(PermissionDenied):
            assert custom_view(mock_request(REMOTE_ADDR='192.168.1.1'))

        assert custom_view(mock_request(REMOTE_ADDR='127.0.0.1'))
