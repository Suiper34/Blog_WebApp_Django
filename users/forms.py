from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as g_l

from .models import User


class SignUpUser(UserCreationForm):
    """
    User creation form requiring unique email and showing password fields in
    UI.

    Internally uses password1/password2 (required by Django) but labels them
    "Password" and "Confirm password" so templates show the expected names.
    """
    email = forms.EmailField(required=True, widget=forms.EmailInput(
        attrs={"class": "form-control"}))

    class Meta:
        model = User
        # keep only username/email in meta so the form renders correctly.
        fields = ("username", "email")
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["password1"].label = g_l("New Password")
        self.fields["password1"].widget = forms.PasswordInput(
            attrs={"class": "form-control"})
        self.fields["password2"].label = g_l("Confirm password")
        self.fields["password2"].widget = forms.PasswordInput(
            attrs={"class": "form-control"})

        self.fields["email"].label = g_l("Email")
        self.fields["username"].label = g_l("Username")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email__iexact=email).exists():
            raise ValidationError(
                g_l('A user with that email already exists!'))
        return email


class LoginUser(AuthenticationForm):
    """
    User login form using username and password.
    """

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                g_l('This account is inactive!'), code='inactive')


class UsersComments(forms.Form):
    comment = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        max_length=1500,
        required=True,
        label='Your comment'
    )
