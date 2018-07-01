from django.contrib import admin
from .models import Server, ConnectionInfo, Database, UploadLog
# Register your models here.


class ConnectInfoInline(admin.StackedInline):
    model = ConnectionInfo


class ServerAdmin(admin.ModelAdmin):
    inlines = [ConnectInfoInline, ]


admin.site.register(Server, ServerAdmin)
admin.site.register(UploadLog)
admin.site.register(Database)
