from django.db import models
from .choices import ConnectionType, ServerType, DatabaseType
from account.models import User
from django.db.models import Q


class Server(models.Model):
    name = models.CharField(max_length=64, blank=False)
    type = models.CharField(max_length=20, choices=ServerType.choices, blank=False)
    map_cycle_location = models.CharField(max_length=128, blank=True)
    map_location = models.CharField(max_length=128, blank=False)
    fast_download_server = models.ForeignKey('self', models.DO_NOTHING, null=True, blank=True, limit_choices_to=Q(type__in=[ServerType.FAST_DL, ServerType.FAST_DL_PUBLIC]))

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


class Database(models.Model):
    name = models.CharField(max_length=30)
    dictionary_name = models.CharField(max_length=30)
    type = models.CharField(max_length=30, choices=DatabaseType.choices)

    def __str__(self):
        return self.name


class UploadLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=False)
    date = models.DateTimeField(auto_now_add=True)
    map_name = models.CharField(max_length=32)
    exception = models.CharField(max_length=10240)
    servers = models.ManyToManyField(Server)
    success = models.BooleanField(default=False)

    def __str__(self):
        servers = ",".join([s.name for s in self.servers.all()])
        return f"{self.user.username} uploaded {self.map_name} on {self.date} to {servers}"


class Map(models.Model):
    mapID = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=45)
    difficulty = models.IntegerField()
    checkpoints = models.IntegerField()
    mapType = models.IntegerField()
    author = models.CharField(max_length=45)
    bonuses = models.IntegerField()
    active = models.BooleanField()
    prehop = models.BooleanField()
    enableBakedTriggers = models.BooleanField()

    class Meta:
        db_table = "cs_maps"
        managed = False


class UploaderPermissions(models.Model):
    class Meta:
        managed = False

        permissions = (
            ("uploader_access", "Has access to the uploader"),
            ("uploader_admin", "Has uploader admin access"),
            ("uploader_surf", "Has access to all the surf servers"),
            ("uploader_bhop", "Has access to all the bhop servers")
        )
