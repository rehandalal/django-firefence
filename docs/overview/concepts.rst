Concepts
========

Rules
-----

A ``Rule`` is the basic building block of django-firefence. They are objects that define what
characterists of a request to match on and what action to take if they match.

You must define an ``action`` for all rules. This ``action`` must be one of either ``'ALLOW'`` or
``'DENY'``.

You may also define a ``host`` for a rule. This host will match against the hostname or the IP
address of the incoming request. This can be a simple hostname of the remote machine(eg:
``'localhost'``), an IPv4 address (eg: ``'192.168.1.1'``), an IPv6 address (eg:
``'2001:0db8:85a3:0000:0000:8a2e:0370:7334'``), an IPv4 subnet in CIDR notation (eg:
``'192.168.1.0/24'``) or and IPv6 subnet in CIDR notation (eg: ``'2001:0db8::/32'``).

Finally, you may define a ``port`` for a rule. This will match the server port that the request is
made to. Typically requests are made to port 80 for HTTP and port 443 for HTTPS but if you have
some kind of non-standard setup you can use this to filter accordingly. The ``port`` can be an
integer or a string (eg: ``80`` or ``'80'``), a string representing a range of ports (eg:
``'80:90'``), a string with a comma-separated list of ports (eg: ``'80, 443'``) or a list or tuple
of integers or strings (eg: ``('80', '443')`` or ``[80, 443]``).

If the ``host`` is not defined the rule will match all IPs or hostnames. Similarly, if the ``port``
is not defined the rule will match all ports. If both are defined, both must match.


RuleSets
--------

``RuleSet``s are an ordered, iterable collection of ``Rule``s. They provide the list of
rules for a request to be matched against. Rules are applied to requests in order. When a request
matches a rule, that rule's action is applied and all subsequent rules are ignored.

If there are no rules in a ``RuleSet`` there is no action taken. If for some reason you wanted to
block all requests you would need to add a rule with the action set to ``'DENY'`` and no host or
port specified.

If a ``RuleSet`` only has rules with ``'DENY'`` as the action, it will allow all requests except
the ones that match one of the rules. However, if there are any rules in a ``RuleSet`` that have
``'ALLOW'`` as an action, then requests are denied by default unless they match an allow-rule.


Fences
------

A ``Fence`` is a backend object that takes a ``RuleSet`` and defines what to do if a denial-rule
is matched. The default backend provided by django-firefence simply raises a ``PermissionDenied``
error when a denial occurs.
