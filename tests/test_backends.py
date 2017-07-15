from firefence.backends import Fence
from firefence.rules import Rule, RuleSet


class TestFence(object):
    def test_set_rules(self):
        """Test setting the rules for a fence."""

        # Test that it accepts a RuleSet
        ruleset = RuleSet([Rule(action=Rule.DENY, host='127.0.0.1')])
        fence = Fence(ruleset)
        assert len(fence.rules) == 1
        assert fence.rules[0].action == Rule.DENY
        assert fence.rules[0].host == '127.0.0.1'

        # Test that you can pass through an array of rules
        fence = Fence([{'action': Rule.ALLOW, 'host': '192.168.1.1'}])
        assert len(fence.rules) == 1
        assert fence.rules[0].action == Rule.ALLOW
        assert fence.rules[0].host == '192.168.1.1'
