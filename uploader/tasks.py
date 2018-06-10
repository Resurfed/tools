from tools.celery import app
from celery.signals import task_failure, task_success
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Server
from .choices import ServerType
from .helpers import websocket_response, compress, MessageHandler
from functools import partial
from .uploader import Uploader, ConnectionFailure, AuthenticationFailure
import os


#@app.task(name="uploader.tasks.upload_map")
def process_map(channel_name, file_path, servers, user):

    message_handler = MessageHandler(channel_name)
    message_handler.send_started_task()

    if not os.path.exists(file_path):
        error = "Uploaded file could not be found"
        message_handler.send_general_error({"error": error})
        raise IOError(error)

    base = os.path.basename(file_path)
    compressed_base = f"{base}.bz2"
    compressed_path = f"{file_path}.bz2"
    used_fastdls = []

    servers = [Server.objects.get(pk=server) for server in servers]

    message_handler.send_message( f"Compressing {base}")

    try:
        compress(file_path, message_handler.send_progress_update)
    except IOError:
        error = "There was an error when compressing the map file"
        message_handler.send_general_error({"error": error})
        raise IOError(error)

    for server in servers:

        server_node = message_handler.add_message_node(server.name)

        uploader = Uploader.factory(server.connectioninfo)
        uploader.set_progress_callback(message_handler.send_progress_update)

        remote_compressed_path = f"{server.map_location}/{compressed_base}" if not server.map_location.endswith("/") \
            else f"{server.map_location}{compressed_base}"

        remote_path = f"{server.map_location}/{base}" if not server.map_location.endswith("/") \
            else f"{server.map_location}{base}"

        try:
            map_node = message_handler.add_sub_item_message_node(server_node, f"Uploading {base}")
            uploader.set_retry_callback(partial(message_handler.send_retry_message, parent_node=map_node))

            while True:
                uploader.connect()
                success = uploader.upload(compressed_path, remote_path)

            if not success:
                pass  # print error message

            if server.fast_download_server is not None:
                message_handler.add_sub_item_message(server_node, f"Uploading {compressed_base}")
                uploader.upload(file_path, remote_compressed_path)
                used_fastdls.append(server.fast_download_server.id)
        except ConnectionFailure as ex:
            message_handler.send_general_error({"error": "Could not connect to the remote server"})
            raise ex
        except AuthenticationFailure as ex:
            message_handler.send_general_error({"error": "Could not authenticate to the remote server"})
            raise ex




#@task_success.connect(sender=upload_map)
def upload_map_success(signal, sender, result, **kwargs):
    print("upload map success!")


#@task_failure.connect(sender=upload_map)
def upload_map_failure( **kwargs):
    print(kwargs)
    print("upload map failed!")

