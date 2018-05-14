import json

from django.contrib.auth import login, logout
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from .forms import RegisterForm
from .models import User
# Create your views here.
'''

/', views.login_user, name=
ter/', views.register_user,
t/', views.logout_user, nam
, views.user_profile, name=

'''


def login_user(request):
    pass


def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():

            user_name = form.cleaned_data.get('user_name')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            user = User.objects.create_user(user_name, email, password)
            user.save()
            login(request, user)
        else:
            return HttpResponse(json.dumps({"success": False, "errors": [form.errors]}),
                                content_type='application/json', status=404)

    return HttpResponse(json.dumps({"success": True, "redirect": reverse('home:index')}),
                        content_type='application/json', status=200)


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('home:index')


def account_profile(request):
    pass