import pytest

from mock import Mock

from firefence.rules import (
    get_remote_host,
    get_remote_ip,
    get_server_port,
    Rule,
    RuleSet,
)

from . import mock_request


class TestUtilityMethods(object):
    def test_get_remote_ip(self):
        request = mock_request(REMOTE_ADDR='1.1.1.1')
        assert get_remote_ip(request) == '1.1.1.1'

        request = mock_request(HTTP_X_FORWARDED_FOR='2.2.2.2, 3.3.3.3')
        assert get_remote_ip(request) == '2.2.2.2'

        request = mock_request(HTTP_X_FORWARDED_FOR='2.2.2.2', REMOTE_ADDR='1.1.1.1')
        assert get_remote_ip(request) == '2.2.2.2'

    def test_get_remote_host(self):
        request = mock_request(REMOTE_HOST='the.host')
        assert get_remote_host(request) == 'the.host'

        request = mock_request(HTTP_X_FORWARDED_HOST='forwarded.host')
        assert get_remote_host(request) == 'forwarded.host'

        request = mock_request(HTTP_X_FORWARDED_HOST='forwarded.host', REMOTE_HOST='the.host')
        assert get_remote_host(request) == 'forwarded.host'

    def test_get_server_port(self):
        request = mock_request(SERVER_PORT='8000')
        assert get_server_port(request) == 8000

        request = mock_request(HTTP_X_FORWARDED_PORT='8000')
        assert get_server_port(request) == 8000

        request = mock_request(HTTP_X_FORWARDED_PORT='8000', SERVER_PORT='80')
        assert get_server_port(request) == 8000

        request = Mock()
        request.META = {}
        assert get_server_port(request) is None

        request.META['SERVER_PORT'] = 'invalid'
        assert get_server_port(request) is None


class TestRule(object):
    def test_str(self):
        rule = Rule(action=Rule.ALLOW)
        assert str(rule) == 'ALLOW'

        rule = Rule(action=Rule.ALLOW, host='1.1.1.1')
        assert str(rule) == 'ALLOW from 1.1.1.1'

        rule = Rule(action=Rule.ALLOW, host='remote.host', port='80')
        assert str(rule) == 'ALLOW from remote.host to 80'

        rule = Rule(action=Rule.ALLOW, port='80:82')
        assert str(rule) == 'ALLOW to 80:82'

    def test_repr(self):
        rule = Rule(action=Rule.ALLOW, host='1.1.1.1')
        assert repr(rule) == '<Rule: ALLOW from 1.1.1.1>'

    def test_rules_must_have_action(self):
        with pytest.raises(ValueError):
            Rule()

    def test_action_validation(self):
        Rule(action='allow')
        Rule(action='AlLoW')
        Rule(action='ALLOW')

        Rule(action='deny')
        Rule(action='dEnY')
        Rule(action='DENY')

        with pytest.raises(ValueError):
            Rule(action='foo')

    def test_port_validation(self):
        rule = Rule(action=Rule.ALLOW, port=80)
        assert rule.port == '80'

        rule = Rule(action=Rule.ALLOW, port='80')
        assert rule.port == '80'

        rule = Rule(action=Rule.ALLOW, port='80:90')
        assert rule.port == '80:90'

        rule = Rule(action=Rule.ALLOW, port='80, 82,84')
        assert rule.port == '80, 82, 84'

        rule = Rule(action=Rule.ALLOW, port=list(range(80, 91)))
        assert rule.port == '80:90'

        rule = Rule(action=Rule.ALLOW, port=(80, 82))
        assert rule.port == '80, 82'

        rule = Rule(action=Rule.ALLOW, port=None)
        assert rule.port is None

        with pytest.raises(TypeError):
            Rule(action=Rule.ALLOW, port=80.0)

    def test_host_matches(self):
        rule = Rule(action=Rule.ALLOW)
        assert rule.host_matches(mock_request())

        # Test hostname matching
        rule = Rule(action=Rule.ALLOW, host='the.host')
        assert rule.host_matches(mock_request(REMOTE_HOST='the.host'))
        assert not rule.host_matches(mock_request(REMOTE_HOST='not.the.host'))
        assert not rule.host_matches(mock_request(REMOTE_HOST='THE.HOST'))

        # Test IPv4 matching
        rule = Rule(action=Rule.ALLOW, host='1.1.1.1')
        assert rule.host_matches(mock_request(REMOTE_ADDR='1.1.1.1'))
        assert not rule.host_matches(mock_request(REMOTE_ADDR='2.2.2.2'))
        assert not rule.host_matches(mock_request(REMOTE_ADDR='1:1:1:1:1:1:1:1'))

        # Test IPv6 matching
        rule = Rule(action=Rule.ALLOW, host='1:1:1:1:1:1:1:1')
        assert rule.host_matches(
            mock_request(REMOTE_ADDR='0001:0001:0001:0001:0001:0001:0001:0001'))
        assert rule.host_matches(mock_request(REMOTE_ADDR='1:1:1:1:1:1:1:1'))
        assert not rule.host_matches(mock_request(REMOTE_ADDR='1:1:1:1:1:1:1:f'))
        assert not rule.host_matches(mock_request(REMOTE_ADDR='2.2.2.2'))

        # Test IPv4 subnet matching
        rule = Rule(action=Rule.ALLOW, host='1.1.1.0/25')
        assert rule.host_matches(mock_request(REMOTE_ADDR='1.1.1.0'))
        assert rule.host_matches(mock_request(REMOTE_ADDR='1.1.1.32'))
        assert rule.host_matches(mock_request(REMOTE_ADDR='1.1.1.127'))
        assert not rule.host_matches(mock_request(REMOTE_ADDR='1.1.1.128'))
        assert not rule.host_matches(mock_request(REMOTE_ADDR='1.1.1.255'))
        assert not rule.host_matches(mock_request(REMOTE_ADDR='1:1:1:1:1:1:1:1'))

        # Test IPv6 subnet matching
        rule = Rule(action=Rule.ALLOW, host='1:1:1:1::/64')
        assert rule.host_matches(mock_request(REMOTE_ADDR='1:1:1:1:0:0:0:0'))
        assert rule.host_matches(mock_request(REMOTE_ADDR='1:1:1:1:ffff:ffff:ffff:ffff'))
        assert not rule.host_matches(mock_request(REMOTE_ADDR='1:1:1:2:0:0:0:0'))

    def test_port_matches(self):
        rule = Rule(action=Rule.ALLOW)
        assert rule.port_matches(mock_request())

        rule = Rule(action=Rule.ALLOW, port=8000)
        assert rule.port_matches(mock_request(SERVER_PORT='8000'))
        assert not rule.port_matches(mock_request(SERVER_PORT='80'))

        rule = Rule(action=Rule.ALLOW, port='8000,8080')
        assert rule.port_matches(mock_request(SERVER_PORT='8000'))
        assert rule.port_matches(mock_request(SERVER_PORT='8080'))
        assert not rule.port_matches(mock_request(SERVER_PORT='80'))
        assert not rule.port_matches(mock_request(SERVER_PORT='8088'))
        assert not rule.port_matches(mock_request(SERVER_PORT='8888'))

        rule = Rule(action=Rule.ALLOW, port='80:90')
        assert rule.port_matches(mock_request(SERVER_PORT='80'))
        assert rule.port_matches(mock_request(SERVER_PORT='85'))
        assert rule.port_matches(mock_request(SERVER_PORT='90'))
        assert not rule.port_matches(mock_request(SERVER_PORT='79'))
        assert not rule.port_matches(mock_request(SERVER_PORT='91'))

    def test_matches(self):
        rule = Rule(action=Rule.ALLOW)
        assert rule.matches(mock_request())

        rule = Rule(action=Rule.ALLOW, host='1.1.1.1')
        assert rule.matches(mock_request(REMOTE_ADDR='1.1.1.1', SERVER_PORT='80'))
        assert rule.matches(mock_request(REMOTE_ADDR='1.1.1.1', SERVER_PORT='8000'))
        assert not rule.matches(mock_request(REMOTE_ADDR='2.2.2.2'))

        rule = Rule(action=Rule.ALLOW, port=8000)
        assert rule.matches(mock_request(REMOTE_ADDR='1.1.1.1', SERVER_PORT='8000'))
        assert rule.matches(mock_request(REMOTE_ADDR='2.2.2.2', SERVER_PORT='8000'))
        assert not rule.matches(mock_request(SERVER_PORT='80'))

        rule = Rule(action=Rule.ALLOW, host='1.1.1.1', port=8000)
        assert rule.matches(mock_request(REMOTE_ADDR='1.1.1.1', SERVER_PORT='8000'))
        assert not rule.matches(mock_request(REMOTE_ADDR='2.2.2.2', SERVER_PORT='8000'))
        assert not rule.matches(mock_request(REMOTE_ADDR='1.1.1.1', SERVER_PORT='80'))


class TestRuleSet(object):
    def test_str(self):
        rs = RuleSet()
        assert str(rs) == ''

        rs = RuleSet([Rule(action=Rule.ALLOW, port=80)])
        assert str(rs) == 'ALLOW to 80'

        rs = RuleSet([Rule(action=Rule.ALLOW, port=80), Rule(action=Rule.ALLOW, port=443)])
        assert str(rs) == 'ALLOW to 80\nALLOW to 443'

    def test_repr(self):
        rs = RuleSet([Rule(action=Rule.ALLOW, port=80)])
        assert repr(rs) == '(<Rule: ALLOW to 80>,)'

    def test_len(self):
        rs = RuleSet()
        assert len(rs) == 0

        rs = RuleSet([Rule(action=Rule.ALLOW, port=80)])
        assert len(rs) == 1

    def test_get_item(self):
        rule = Rule(action=Rule.ALLOW, port=80)

        rs = RuleSet([rule])
        assert rs[0] == rule

        with pytest.raises(IndexError):
            assert rs[1]

    def test_iter(self):
        rules = [
            Rule(action=Rule.ALLOW, port=80),
            Rule(action=Rule.ALLOW, port=443),
        ]
        rs = RuleSet(rules)

        for index, rule in enumerate(rs):
            assert rule == rules[index]

    def test_rules_validation(self):
        rs = RuleSet()
        assert rs.rules == ()

        with pytest.raises(TypeError):
            rs.rules = Rule(action=Rule.ALLOW)

        rs.rules = [Rule(action=Rule.ALLOW)]
        assert len(rs.rules) == 1
        assert rs.rules[0].action == Rule.ALLOW

        rs.rules = [{'action': Rule.ALLOW}]
        assert len(rs.rules) == 1
        assert rs.rules[0].action == Rule.ALLOW

        with pytest.raises(TypeError):
            rs.rules = ['allow']

    def test_allows(self):
        # No rules should always allow requests
        rs = RuleSet()
        assert rs.allows(mock_request())

        # Allow all requests
        rs = RuleSet([Rule(action=Rule.ALLOW)])
        assert rs.allows(mock_request())

        # Deny all requests
        rs = RuleSet([Rule(action=Rule.DENY)])
        assert not rs.allows(mock_request())

        # Allow only requests from 1.1.1.1
        rs = RuleSet([Rule(action=Rule.ALLOW, host='1.1.1.1')])
        assert rs.allows(mock_request(REMOTE_ADDR='1.1.1.1'))
        assert not rs.allows(mock_request(REMOTE_ADDR='2.2.2.2'))

        # Deny only requests from 1.1.1.1
        rs = RuleSet([Rule(action=Rule.DENY, host='1.1.1.1')])
        assert not rs.allows(mock_request(REMOTE_ADDR='1.1.1.1'))
        assert rs.allows(mock_request(REMOTE_ADDR='2.2.2.2'))

        # Allow only requests from 1.1.1.1 except to port 8000
        rs = RuleSet([
            Rule(action=Rule.DENY, host='1.1.1.1', port=8000),
            Rule(action=Rule.ALLOW, host='1.1.1.1'),
        ])
        assert rs.allows(mock_request(REMOTE_ADDR='1.1.1.1', SERVER_PORT=80))
        assert not rs.allows(mock_request(REMOTE_ADDR='1.1.1.1', SERVER_PORT=8000))
        assert not rs.allows(mock_request(REMOTE_ADDR='2.2.2.2'))
