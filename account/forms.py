from django import forms
from django.core.exceptions import ValidationError

from .validators import alphanumeric
from .models import User


def set_field_html_name(cls, new_name):
    """
    This creates wrapper around the normal widget rendering,
    allowing for a custom field name (new_name).
    """
    old_render = cls.widget.render

    def _widget_render_wrapper(name, value, attrs=None):
        return old_render(new_name, value, attrs)

    cls.widget.render = _widget_render_wrapper


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
        required=False,
        validators=[alphanumeric],
        widget=forms.TextInput(
            attrs={
                'id': 'id_register_user_name',
                'placeholder': 'Username',
                'class': 'form-control',
                'tabindex': 1
            }
        )
    )

    set_field_html_name(user_name, 'register_user_name')

    email = forms.EmailField(
        max_length=50,
        required=True,
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Email Address',
                'class': 'form-control',
                'tabindex': 2
            }
        )
    )

    password = forms.CharField(
        max_length=64,
        required=False,
        widget=forms.PasswordInput(
            attrs={
                'id': 'id_register_password',
                'placeholder': 'Password',
                'class': 'form-control',
                'tabindex': 3
            }
        )
    )

    set_field_html_name(password, 'register_password')

    confirm_password = forms.CharField(
        max_length=64,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'id': 'id_register_confirm_password',
                'placeholder': 'Confirm Password',
                'class': 'form-control',
                'tabindex': 4
            }
        )
    )

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match')
        return self.cleaned_data

    def clean_password(self):
        data = self.data['register_password']
        if data is None:
            raise ValidationError('Missing password')
        return data

    def clean_user_name(self):
        data = self.data['register_user_name']
        if data is None:
            raise ValidationError('Missing user name')

        try:
            User.objects.get(username=data)
        except User.DoesNotExist:
            return data

        raise ValidationError("This username is already taken")

    def clean_email(self):
        data = self.data['email']
        if data is None:
            raise ValidationError('Missing user name')

        try:
            User.objects.get(email=data)
        except User.DoesNotExist:
            return data

        raise ValidationError("This email address is already taken")

    class Meta:
        model = User
        fields = {'user_name', 'email', 'register_password', 'confirm_password'}