from django.conf.urls import url

from . import views
from . import consumers

app_name = "uploader"
urlpatterns = [

    url(r'^$', views.uploader, name='uploader'),
    url(r'^disabled/$', views.disabled, name='disabled')
]

websocket_urlpatterns = [
    url(r'^ws/uploader$', consumers.UploadConsumer)
]