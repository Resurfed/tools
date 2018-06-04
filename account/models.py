from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
import datetime
import pytz

# Create your models here.


class User(AbstractUser):
    steam_id = models.CharField(default='', blank=True, max_length=20)
    enabled = models.BooleanField(default=False)


class ResetPasswordToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    def is_expired(self):
        expired = (datetime.datetime.now() + datetime.timedelta(minutes=60)).replace(tzinfo=pytz.UTC)
        return expired >= self.created

    def __str__(self):
        return f"Reset token for {self.user.username} (Created: {self.created})"
