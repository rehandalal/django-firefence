Decorator
=========

django-firefence comes with a view decorator that you can use to protect individual views.

This decorator allows you to specify a set of rules to use as well what backend class to use. If
either is not provided the defaults specified in the settings will be used.

Here are some examples of how to use the decorator

    .. code-block:: python

        from firefence.decorators import fence_protected
        from firefence.rules import Rule

        from my_project.firefence_backends import CustomFence


        # Use the default rules and backend
        @fence_protected()
        def my_view(request):
            return render(request, 'template.html')


        # Use a custom set of rules
        @fence_protected(rules=[
            Rule(action=Rule.ALLOW, host='192.168.1.1')
        ])
        def another_view(request):
            return render(request, 'template.html')


        # Use a custom backend
        @fence_protected(backend_class=CustomFence)
        def third_view(request):
            return render(request, 'template.html')
