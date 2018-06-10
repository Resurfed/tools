from channels.generic.websocket import JsonWebsocketConsumer
from .helpers import USER_CHANNEL_NAME
import json


class UploadConsumer(JsonWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def connect(self):
        self.accept()
        self.user = self.scope['user']
        USER_CHANNEL_NAME.update({self.user.id: self.channel_name})

    def disconnect(self, close_code):
        USER_CHANNEL_NAME.pop(self.user.id)
        pass

    def receive_json(self, content, **kwargs):
        pass

    def send_message(self, message):
        message.pop('type')
        self.send(text_data=json.dumps(message))


# async_to_sync(channel_layer.send)("specific.IfBPLGNj!iiPqBRAGDSIf", {"message": "hello", "type": "send_thing"})