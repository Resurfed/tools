from django import forms
from .validators import alphanumeric


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