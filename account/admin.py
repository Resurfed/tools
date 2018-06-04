from django.contrib import admin
from .models import User, ResetPasswordToken
from django.contrib.auth.admin import UserAdmin
# Register your models here.


class ResetEmailAdmin(admin.ModelAdmin):
    readonly_fields = ['token', 'created']


admin.site.register(User, UserAdmin)
admin.site.register(ResetPasswordToken, ResetEmailAdmin)