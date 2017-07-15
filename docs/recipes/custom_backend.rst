Custom Backend
==============

The provided ``Fence`` backend raises a ``PermissionDenied`` error when a denial occurs. If this
is not the desired behaviour, you must use a custom backend.

To make the process easy we provide a ``AbstractFence`` class that you can extend to easily create
new backends. All you have to do is implement a ``reject`` method on the new backend. This method
must either raise an exception that Django can handle or return an ``HttpResponse`` object.

    .. code-block:: python

        from firefence.backends import AbstractFence


        class CustomFence(AbstractFence):
            def reject(self, request):
                return render(request, 'denied.html')
