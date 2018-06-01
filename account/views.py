import json

from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from .forms import RegisterForm, LoginForm, SendResetPasswordForm, ResetPasswordForm
from .models import User, ResetEmail
import requests
from django.db.utils import IntegrityError

# Create your views here.
'''

/', views.login_user, name=
ter/', views.register_user,
t/', views.logout_user, nam
, views.user_profile, name=

'''


def login_user(request):
    if request.user.is_authenticated:
        return redirect('home:index')

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            user_name = form.cleaned_data.get('user_name')
            password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get('remember_me')

            user = authenticate(username=user_name, password=password)

            if user is not None:
                if not remember_me:
                    request.session.set_expiry(0)
                login(request, user)

                next_url = request.POST.get('next')

                if next_url is None:
                    next_url = reverse('home:index')
                return HttpResponse(json.dumps({"success": True, 'redirect': next_url}),
                                    content_type='application/json')

            else:
                return HttpResponse(json.dumps({"success": False, "errors": ["Invalid username or password"]}),
                                    content_type='application/json')

        else:
            errors = []
            for item in form.errors:
                errors = [err for err in form.errors[item]]
            return HttpResponse(json.dumps({"success": False, "errors": errors}),
                                content_type='application/json', status=404)

    return render(request, 'account/login.html', {
        'form': LoginForm()
    })


def register_user(request):
    if request.user.is_authenticated:
        return redirect('home:index')

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
            errors = []
            for item in form.errors:
                errors += [err for err in form.errors[item]]

            return HttpResponse(json.dumps({"success": False, "errors": errors}),
                                content_type='application/json', status=404)

    return render(request, 'account/register.html', {
        'form': RegisterForm()
    })


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('home:index')


def forget_password(request):
    if request.method == 'POST':
        form = SendResetPasswordForm(request.POST)

        if form.is_valid():

            email = form.cleaned_data.get('email')

            user = User.objects.filter(email=email).first()
            reset = ResetEmail.objects.filter(user=user).first()

            if reset is not None:
                reset.delete()

            reset = ResetEmail()
            reset.user = user
            reset.save()

            key = 'PUT KEY HERE'
            request_url = 'https://api.mailgun.net/v3/mail.resurfed.com/messages'
            reset_link = f"http://tools.resurfed.xyz/account/reset/{reset.code}"

            request = requests.post(request_url, auth=('api', key), data={
                'from': 'mail.resurfed.com',
                'to': email,
                'subject': 'ReSurfed tools password reset',
                'text': f"You somehow forgot your own password. Click <a href='{reset_link}'>Here</a> to reset it."
            })

            if request.status_code != 200:
                return HttpResponse(json.dumps({"success": False, "errors": ['Unable to send email']}),
                                    content_type='application/json', status=404)

            return HttpResponse(json.dumps({"success": True}),
                                content_type='application/json')
        else:
            errors = []
            for item in form.errors:
                errors = [err for err in form.errors[item]]

            return HttpResponse(json.dumps({"success": False, "errors": errors}),
                                content_type='application/json', status=404)

    return render(request, 'account/forget-password.html', {
        'form': SendResetPasswordForm()
    })


def reset_password(request, code):

    return render(request, 'account/reset-password.html', {
        'form': ResetPasswordForm(code=code),
        'code': code
    })


def account_profile(request):
    pass
