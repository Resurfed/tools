from django.shortcuts import render
from account.forms import LoginForm, RegisterForm, SendResetPasswordForm

# Create your views here.


def index(request):
    login_form = LoginForm()
    register_form = RegisterForm()
    send_reset_form = SendResetPasswordForm()

    return render(request, 'index.html', {
        "login_form": login_form,
        "register_form": register_form,
        "send_reset_form": send_reset_form
    })

