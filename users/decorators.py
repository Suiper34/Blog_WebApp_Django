from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect


def admins_only(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Login required")
            return redirect('login')
        if not getattr(request.user, 'is_admin', lambda: False)():
            messages.error(request, "Admins only!")
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
