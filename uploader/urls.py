from django.conf.urls import url

from . import views

app_name = "uploader"
urlpatterns = [

    url(r'^', views.uploader, name='uploader'),
]
