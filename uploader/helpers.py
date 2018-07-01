import json
import tempfile
import os
import bz2
from .choices import ActionType
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import uuid


def handle_uploaded_file(f):
    path = os.path.join(tempfile.gettempdir(), f.name)
    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return path


def compress(file_path, callback):
    total_size = os.path.getsize(file_path)
    compressed_path = f"{file_path}.bz2"

    with open(file_path, 'rb') as uncompressed_file, bz2.BZ2File(compressed_path, 'wb') as compressed_file:
        for data in iter(lambda: uncompressed_file.read(3 * 1000 * 1024), b''):
            compressed_file.write(data)
            percent_complete = round((uncompressed_file.tell() / total_size) * 100)

            callback(percent_complete)


def generate_id():
    return uuid.uuid4().hex[:10]


class MessageHandler:

    def __init__(self, channel_name):
        self.channel_name = channel_name
        self.layer = get_channel_layer()

    @staticmethod
    def format_packet(action, data=None):
        t = {
            "action": action,
            "type": "send_message"
        }
        if data is not None:
            t.update(data)

        return t

    def __send(self, message):
        async_to_sync(self.layer.send)(self.channel_name, message)

    def send_message(self, message):
        self.__send(self.format_packet(ActionType.MESSAGE, {"message": message}))

    def send_progress_update(self, progress):
        self.__send(self.format_packet(ActionType.PROGRESS_UPDATE, {"progress": progress}))

    def send_general_error(self, error):
        self.__send(self.format_packet(ActionType.GENERAL_ERROR, error))

    def send_started_task(self):
        self.__send(self.format_packet(ActionType.STARTED_TASK))

    def add_message_node(self, message):
        node_id = generate_id()
        self.__send(self.format_packet(ActionType.LIST, {"id": node_id, "message": message}))
        return node_id

    def add_sub_item_message(self, node_id, message):
        self.__send(self.format_packet(ActionType.SUB_ITEM, {"id": node_id, "message": message}))

    def add_sub_item_message_node(self, parent_node, message):
        node_id = generate_id()
        self.__send(self.format_packet(ActionType.SUB_LIST, {"parent": parent_node, "id": node_id,
                                                             "message": message}))
        return node_id

    def send_retry_message(self, message, parent_node):
        self.add_sub_item_message(parent_node, message)
