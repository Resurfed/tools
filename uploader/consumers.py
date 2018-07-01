from channels.generic.websocket import JsonWebsocketConsumer
from .helpers import MessageHandler
from .choices import ActionType
import json


class UploadConsumer(JsonWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def connect(self):
        self.accept()
        self.user = self.scope['user']
        self.send_message(MessageHandler.format_packet(ActionType.CHANNEL_NAME, {"channel": self.channel_name}))

    def disconnect(self, close_code):
        pass

    def receive_json(self, content, **kwargs):
        pass

    def send_message(self, message):
        message.pop('type')
        self.send(text_data=json.dumps(message))


# async_to_sync(channel_layer.send)("specific.IfBPLGNj!iiPqBRAGDSIf", {"message": "hello", "type": "send_thing"})