import ipcalc


def get_remote_ip(request):
    xff = request.META.get('HTTP_X_FORWARDED_FOR')
    return xff.split(',').pop() if xff else request.META.get('REMOTE_ADDR')


def get_remote_host(request):
    return request.META.get('HTTP_X_FORWARDED_HOST', request.META.get('REMOTE_HOST'))


def get_server_port(request):
    return request.META.get('HTTP_X_FORWARDED_PORT', request.META.get('SERVER_PORT'))


class Rule(object):
    ALLOW = 'ALLOW'
    DENY = 'DENY'

    _action = None
    _ports = ()

    def __init__(self, **kwargs):
        if 'action' not in kwargs:
            raise ValueError('Rules must have an action.')
        self.action = kwargs.get('action')
        self.address = kwargs.get('address')
        self.port = kwargs.get('port')

    def __str__(self):
        str = self.action
        if self.address:
            str += ' from {}'.format(self.address)
        if self.port:
            str += ' to {}'.format(self.port)
        return str

    def __repr__(self):
        return '<Rule: {}>'.format(self)

    @property
    def action(self):
        return self._action

    @action.setter
    def action(self, value):
        if value.upper() not in (self.ALLOW, self.DENY):
            raise ValueError('Action must be ALLOW or DENY.')
        self._action = value.upper()

    @property
    def port(self):
        if self._ports:
            if len(self._ports) == 1:
                return str(self._ports[0])
            else:
                if set(self._ports) == set(range(self._ports[0], self._ports[-1] + 1)):
                    return '{}:{}'.format(self._ports[0], self._ports[-1])
                else:
                    return ', '.join([str(port) for port in self._ports])
        return None

    @port.setter
    def port(self, value):
        if value is None:
            self._ports = ()
        else:
            ports = str(value).split(',')
            if len(ports) == 1:
                ports = ports[0].split(':', 1)

                if len(ports) == 1:
                    self._ports = (int(ports[0]),)
                else:
                    self._ports = tuple(range(int(ports[0]), int(ports[1]) + 1))
            else:
                self._ports = tuple(sorted([int(port) for port in set(ports)]))

    def address_matches(self, request):
        remote_ip = get_remote_ip(request)
        remote_host = get_remote_host(request)

        if self.address:
            if remote_host == self.address:
                return True

            try:
                return remote_ip in ipcalc.Network(self.address)
            except ValueError:
                return False

        return True

    def port_matches(self, request):
        server_port = get_server_port(request)
        return server_port in self._ports if self.port else True

    def matches(self, request):
        return self.address_matches(request) and self.port_matches(request)


class RuleSet(object):
    _rules = ()

    def __init__(self, rules=None):
        self.rules = rules

    def __len__(self):
        return len(self.rules)

    def __getitem__(self, index):
        return self.rules[index]

    def __iter__(self):
        return self.rules.__iter__()

    def __str__(self):
        return '\n'.join([str(rule) for rule in self.rules])

    def __repr__(self):
        return '<RuleSet: {} rules>'.format(len(self.rules))

    @property
    def rules(self):
        return self._rules

    @rules.setter
    def rules(self, value):
        if value is None:
            self._rules = ()
        else:
            if not isinstance(value, (list, tuple)):
                raise TypeError('Expected a list or tuple of rules.')

            rules = []
            for rule in value:
                if isinstance(rule, Rule):
                    rules.append(rule)
                elif isinstance(rule, dict):
                    rules.append(Rule(**rule))
                else:
                    raise TypeError('Expected a Rule or dict.')
            self._rules = tuple(rules)

    def allows(self, request):
        default = True

        for rule in self.rules:
            if rule.action == Rule.DENY and rule.matches(request):
                return False
            elif rule.action == Rule.ALLOW:
                # Change the default if an ALLOW rule exists
                default = False

                if rule.matches(request):
                    return True

        return default
