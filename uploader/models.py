from django.db import models
from .choices import ConnectionType, ServerType


class Server(models.Model):
    name = models.CharField(max_length=64, blank=False)
    server_type = models.CharField(max_length=20, choices=ServerType.choices, blank=False)
    map_cycle_location = models.CharField(max_length=64, blank=True)
    map_location = models.CharField(max_length=64, blank=False)
    home_location = models.CharField(max_length=64)
    fast_download_server = models.ForeignKey('self', models.DO_NOTHING,null=True, blank=True)

    def __str__(self):
        return f'{self.name}'


class ConnectionInfo(models.Model):
    server = models.OneToOneField(Server, on_delete=models.CASCADE, primary_key=True)
    connection = models.CharField(max_length=10, choices=ConnectionType.choices, blank=False)
    username = models.CharField(max_length=64, blank=False)
    password = models.CharField(max_length=64, blank=False)
    host_address = models.CharField(max_length=32, blank=False)
    port = models.IntegerField()

    def __str__(self):
        return ''

    class Meta:
        verbose_name_plural = "Connection Info"


class UploaderPermissions(models.Model):
    class Meta:
        managed = False

        permissions = (
            ("uploader_access", "Has access to the uploader"),
            ("uploader_admin", "Has uploader admin access"),
            ("uploader_surf", "Has access to all the surf servers"),
            ("uploader_bhop", "Has access to all the bhop servers")
        )
