from django.conf.urls import url

from . import views
from . import consumers

app_name = "uploader"
urlpatterns = [

    url(r'^', views.uploader, name='uploader'),
]

websocket_urlpatterns = [
    url(r'^ws/uploader$', consumers.UploadConsumer)
]