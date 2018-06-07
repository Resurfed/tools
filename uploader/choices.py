import requests
from django.conf import settings
from djchoices import DjangoChoices, ChoiceItem


class ConnectionType(DjangoChoices):
    FTP = ChoiceItem()
    FTPS = ChoiceItem()
    SFTP = ChoiceItem()


class ServerType(DjangoChoices):
    FAST_DL = ChoiceItem()
    FAST_DL_PUBLIC = ChoiceItem()
    SERVER = ChoiceItem()
    SERVER_PUBLIC = ChoiceItem()


class MapType(DjangoChoices):
    LINEAR = ChoiceItem('Linear')
    STAGED = ChoiceItem('Staged')


MapTypeChoices = (
    (0, MapType.STAGED),
    (1, MapType.LINEAR)
)


class ActionType(DjangoChoices):
    GENERAL_ERROR = ChoiceItem("general_error")
    STARTED_TASK = ChoiceItem("started_task")
    FORM_ERROR = ChoiceItem("form_error")
    PROGRESS_UPDATE = ChoiceItem("progress_update")
    REPLY_CHANNEL = ChoiceItem("reply_channel")
    MESSAGE = ChoiceItem("message")


def get_live_maps():

    maps = []

    for url in settings.LIVE_MAP_URLS:
        r = requests.get(url)
        if r.status_code == 200:
            maps += r.text.split('\n')
    return maps
