from django.shortcuts import render
from account.forms import LoginForm

# Create your views here.


def index(request):
    login_form = LoginForm()
    return render(request, 'index.html', {"login_form": login_form})

