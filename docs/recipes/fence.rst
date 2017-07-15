Fence
=====

Sometimes you may have a common set of rules you wish to apply to a number of views. One way that
you could do this is to create an instance of the ``Fence`` backend with those rules and use it
to decorate the views:

    .. code-block:: python

        from firefence.backends import Fence
        from firefence.rules import Rule


        fence = Fence([
            Rule(action=Rule.DENY, host='192.168.1.1', port=80),
            Rule(action=Rule.ALLOW, port=[80, 443]),
        ])


        @fence.protect
        def my_view(request):
            return render(request, 'template.html')


        @fence.protect
        def another_view(request):
            return render(request, 'template.html')
