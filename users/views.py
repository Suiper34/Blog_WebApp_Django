import logging
import smtplib
from typing import Any

from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import \
    PasswordResetConfirmView as DjangoPasswordResetConfirmView
from django.contrib.auth.views import \
    PasswordResetView as DjangoPasswordResetView
from django.core.mail import BadHeaderError
from django.db import IntegrityError, transaction
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext

from .forms import LoginUser, SignUpUser

logger = logging.getLogger(__name__)
User = get_user_model()


def register(request: HttpRequest) -> HttpResponse:
    """Register a new user. Redirects authenticated users to home."""

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = SignUpUser(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = form.save(commit=False)
                    user.username = user.username.strip()
                    user.email = user.email.lower().strip()
                    user.save()
                messages.success(
                    request, 'Account registered successfully! Please login.')
                return redirect('login')
            except IntegrityError:
                messages.error(
                    request,
                    'A user with that username or email already exists!')
            except Exception:
                messages.error(
                    request, 'An unexpected error occurred...Try again later.')
        else:
            # form invalid
            messages.error(request, 'Please fix the errors below.')
    else:
        form = SignUpUser()

    return render(request, 'register.html', {'form': form})


def login_view(request: HttpRequest) -> HttpResponse:
    """Authenticate and log in a user. Redirects authenticated users to home"""

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = LoginUser(request, data=request.POST)
        if form.is_valid():
            try:
                user = form.get_user()
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                next_url = request.GET.get('next') or request.POST.get(
                    'next') or reverse('home')
                return redirect(next_url)
            except Exception:
                messages.error(
                    request, 'Login failed due to an unexpected error!')
        else:
            messages.error(request, 'Invalid credentials! Please try again.')
    else:
        form = LoginUser(request)

    return render(request, 'login.html', {'form': form})


@login_required
def logout_view(request: HttpRequest) -> HttpResponse:
    """
    Log out the user. Accept POST for logout; GET will redirect home to avoid 405.
    Using POST for logout is the recommended secure pattern.
    """
    if request.method == "POST":
        try:
            auth_logout(request)
        except Exception:
            messages.error(request, "Logout failed. Please try again.")
            return redirect("home")
        messages.success(request, "You have been logged out.")
        return redirect("home")
    # Avoid 405 on GET: redirect to home (or render a confirmation page if preferred)
    return redirect("home")


class PasswordResetView(DjangoPasswordResetView):
    """Send password-reset email"""

    template_name = 'registration/password_reset_form.html'
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')
    from_email = None  # uses DEFAULT_FROM_EMAIL if None

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
        except (smtplib.SMTPException, BadHeaderError):
            logger.exception('Failed to send password reset email')
            messages.error(self.request, gettext(
                'Unable to send reset email right now. Try again later.'))
            return redirect(reverse('password_reset'))
        except Exception:
            logger.exception(
                'Unexpected error while sending password reset email')
            messages.error(self.request, gettext(
                'An unexpected error occurred. Try again later.'))
            return redirect(reverse('password_reset'))
        else:
            messages.success(self.request, gettext(
                'If an account with that email exists,\
                    a password reset link was sent.'))
            return response


class PasswordResetConfirmView(DjangoPasswordResetConfirmView):
    """Confirm token and allow setting a new password."""

    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
        except Exception:
            logger.exception('Error while setting new password')
            messages.error(self.request, gettext(
                'Could not set new password. Please try again.'))
            return redirect(reverse('password_reset'))
        else:
            messages.success(self.request, gettext(
                'Your password has been changed. You can now sign in.'))
            return response
