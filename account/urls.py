from django.conf.urls import url

from . import views

app_name = "account"
urlpatterns = [

    url(r'^login/', views.login_user, name='account-login'),
    url(r'^register/', views.register_user, name='account-register'),
    url(r'^logout/', views.logout_user, name='account-logout'),
    url(r'^view', views.account_profile, name='account-profile'),
]
