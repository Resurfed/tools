from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, reverse
from .forms import RegisterForm, LoginForm, SendResetPasswordForm, ResetPasswordForm
from .models import User, ResetPasswordToken
from .responses import ajax_response
from django.conf import settings
import requests


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

                return ajax_response(True, redirect=next_url)

            else:
                return ajax_response(False, 401, errors=["Invalid username or password"])

        else:
            errors = []
            for item in form.errors:
                errors = [err for err in form.errors[item]]
            return ajax_response(False, 400, errors=errors)

    return render(request, 'account/login.html', {
        'form': LoginForm(),
        'next': request.GET.get('next')
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

            return ajax_response(False, 400, errors=errors)

    return render(request, 'account/register.html', {
        'form': RegisterForm()
    })


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('home:index')


def forget_password(request):
    if request.user.is_authenticated:
        return redirect('home:index')

    if request.method == 'POST':
        form = SendResetPasswordForm(request.POST)

        if form.is_valid():

            email = form.cleaned_data.get('email')

            user = User.objects.filter(email=email).first()
            reset = ResetPasswordToken.objects.filter(user=user).first()

            if reset is not None:
                reset.delete()

            reset = ResetPasswordToken()
            reset.user = user
            reset.save()

            key = settings.MAILGUN_API_KEY
            request_url = 'https://api.mailgun.net/v3/mail.resurfed.com/messages'
            reset_link = f"http://tools.resurfed.xyz/account/reset/{reset.token}/"

            request = requests.post(request_url, auth=('api', key), data={
                'from': 'mail.resurfed.com',
                'to': email,
                'subject': 'ReSurfed tools password reset',
                'text': f"You somehow forgot your own password. Click <a href='{reset_link}'>Here</a> to reset it."
            })

            if request.status_code != 200:
                return ajax_response(False, 400, errors=['Unable to send email'])

            return ajax_response(True)
        else:
            errors = []
            for item in form.errors:
                errors = [err for err in form.errors[item]]

            return ajax_response(False, 400, errors=errors)

    return render(request, 'account/forget-password.html', {
        'form': SendResetPasswordForm()
    })


def reset_password(request, token=None):
    if request.user.is_authenticated:
        return redirect('home:index')

    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            token = form.cleaned_data.get('token')
            password = form.cleaned_data.get('password')

            reset = ResetPasswordToken.objects.get(token=token)

            if reset.is_expired():
                return ajax_response(False, 401, errors=['Expired reset token'])

            reset.user.set_password(password)
            reset.user.save()
            reset.delete()

            return ajax_response(True)

        else:
            errors = []
            for item in form.errors:
                errors = [err for err in form.errors[item]]

            return ajax_response(False, 400, errors=errors)

    return render(request, 'account/reset-password.html', {
        'form': ResetPasswordForm(token=token)
    })


def account_profile(request):
    pass
