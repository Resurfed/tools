from django.shortcuts import render
from account.forms import LoginForm, RegisterForm

# Create your views here.


def index(request):
    login_form = LoginForm()
    register_form = RegisterForm()
    return render(request, 'index.html', {"login_form": login_form, "register_form": register_form})

