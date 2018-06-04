from django import forms
from django.utils.safestring import mark_safe

from .validators import alphanumeric
from .models import User, ResetPasswordToken


class LoginForm(forms.Form):
    user_name = forms.CharField(
        max_length=30,
        required=True,
        validators=[alphanumeric],
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Username',
                'tabindex': 1
            }
        )
    )

    password = forms.CharField(
        max_length=64,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password',
                'tabindex': 2
            }
        )
    )

    remember_me = forms.BooleanField(
        help_text="Remember me",
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'tabindex': 3
            }
        )
    )

    class Meta:
        fields = {'user_name', 'password', 'remember_me'}


class RegisterForm(forms.Form):

    user_name = forms.CharField(
        max_length=30,
        required=True,
        validators=[alphanumeric],
        widget=forms.TextInput(
            attrs={
                'id': 'id_register_user_name',
                'placeholder': 'Username',
                'tabindex': 1
            }
        )
    )

    email = forms.EmailField(
        max_length=50,
        required=True,
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Email Address',
                'tabindex': 2
            }
        )
    )

    password = forms.CharField(
        max_length=64,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password',
                'tabindex': 3
            }
        )
    )

    confirm_password = forms.CharField(
        max_length=64,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Confirm Password',
                'tabindex': 4
            }
        )
    )

    def clean(self):
        cleaned_data = super().clean()
        username = self.cleaned_data.get("user_name")
        email = self.cleaned_data.get("email")
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        try:
            User.objects.get(username=username)
            self.add_error('user_name', 'This username is already taken')
        except User.DoesNotExist:
            pass

        try:
            User.objects.get(email=email)
            self.add_error('email', 'This email is already taken')
        except User.DoesNotExist:
            pass

        if password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match')

        return self.cleaned_data

    class Meta:
        model = User
        fields = {'user_name', 'email', 'password', 'confirm_password'}


class SendResetPasswordForm(forms.Form):

    user_name = forms.CharField(
        max_length=30,
        required=True,
        validators=[alphanumeric],
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Username',
                'tabindex': 1
            }
        )
    )

    email = forms.EmailField(
        max_length=50,
        required=True,
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Email Address',
                'tabindex': 1
            }
        )
    )

    def clean(self):
        email = self.cleaned_data.get('email')
        user_name = self.cleaned_data.get('user_name')

        if not User.objects.filter(email=email, username=user_name).exists():
            self.add_error('username', "Could not find an account matching this username and email.")

        return self.cleaned_data

    class Meta:
        fields = {'username', 'email'}


class ResetPasswordForm(forms.Form):

    token = forms.UUIDField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Reset token',
                'tabindex': 1
            }
        )
    )

    password = forms.CharField(
        max_length=64,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'New Password',
                'tabindex': 3
            }
        )
    )

    confirm_password = forms.CharField(
        max_length=64,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Confirm New Password',
                'tabindex': 4
            }
        )
    )

    def __init__(self, *args, **kwargs):
        token = kwargs.pop('token', None)
        super().__init__(*args, **kwargs)
        if token is not None:
            self.fields['token'].initial = mark_safe(token)

    def clean(self):
        cleaned_data = super().clean()
        token = cleaned_data.get('token')
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        try:
            ResetPasswordToken.objects.get(token=token)
        except ResetPasswordToken.DoesNotExist:
            self.add_error('token', 'Invalid password reset code')

        if password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match')

        return self.cleaned_data

    class Meta:
        fields = ('token', 'password', 'confirm_password')