from django.contrib import admin
from .models import User, ResetEmail
from django.contrib.auth.admin import UserAdmin
# Register your models here.


class ResetEmailAdmin(admin.ModelAdmin):
    readonly_fields = ['code']


admin.site.register(User, UserAdmin)
admin.site.register(ResetEmail, ResetEmailAdmin)