from functools import wraps
from typing import Callable

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect


def admins_only(
        view_func: Callable[..., HttpResponse]) -> Callable[..., HttpResponse]:
    """
    Allow only admin users (superuser, staff or role=='admin').
    """
    @wraps(view_func)
    def _wrapped_view(request: HttpRequest, *args, **kwargs) -> HttpResponse:
        # if user not authenticated redirect to login
        if not getattr(
                request, 'user', None) or not request.user.is_authenticated:
            messages.error(request, 'Please sign in to access that page.')
            return redirect('login')

        try:
            is_admin = (
                request.user.is_superuser
                or request.user.is_staff
                or getattr(request.user, 'role', '') == 'admin'
            )
        except Exception:
            is_admin = False

        if not is_admin:
            messages.error(
                request, 'You do not have permission to perform that action.')
            return redirect('home')

        return view_func(request, *args, **kwargs)

    return _wrapped_view
