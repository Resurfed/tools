from tools.celery import app
from celery.signals import task_failure, task_success
from account.models import User
from .models import Server, Map, Database, UploadLog
from .helpers import compress, MessageHandler
from functools import partial
from .uploader import Uploader, ConnectionFailure, AuthenticationFailure, TransmissionError
import os
from os.path import splitext
import tempfile
import uuid
from pathlib import Path
from django.db.utils import IntegrityError


@app.task(name="uploader.tasks.upload_map")
def process_map(channel_name, file_path, servers, user_id):

    message_handler = MessageHandler(channel_name)
    message_handler.send_started_task()
    log = UploadLog()

    if not os.path.exists(file_path):
        error = "Uploaded file could not be found"
        message_handler.send_general_error({"error": error})
        raise IOError(error)

    base = os.path.basename(file_path)
    compressed_base = f"{base}.bz2"
    compressed_path = f"{file_path}.bz2"
    used_fast_dls = []

    servers = [Server.objects.get(pk=server) for server in servers]
    user = User.objects.get(pk=user_id)

    log.user = user
    log.save()  # save for many to many
    log.servers.set(servers)
    log.map_name = base

    message_handler.send_message(f"Compressing {base}")

    try:
        compress(file_path, message_handler.send_progress_update)
    except IOError as ex:
        error = "There was an error when compressing the map file"
        message_handler.send_general_error({"error": error})
        log.exception = ex
        log.save()
        raise IOError(error)

    for server in servers:

        server_node = message_handler.add_message_node(server.name)

        uploader = Uploader.factory(server.connectioninfo)
        uploader.set_progress_callback(message_handler.send_progress_update)

        remote_compressed_path = Path(server.map_location) / compressed_base

        remote_path = Path(server.map_location) / base

        try:
            map_node = message_handler.add_sub_item_message_node(server_node, f"Uploading {base}")
            uploader.set_retry_callback(partial(message_handler.send_retry_message, parent_node=map_node))

            uploader.connect()
            uploader.upload(file_path, remote_path)

            temp_map_cycle = Path(tempfile.gettempdir()) / uuid.uuid4().hex

            uploader.download(server.map_cycle_location, temp_map_cycle)

            if os.path.exists(temp_map_cycle):
                haystack = []
                needle = splitext(base)[0]
                with open(temp_map_cycle, 'r') as map_cycle:
                    for line in map_cycle:
                        haystack.append(line.strip())

                if needle not in haystack:
                    haystack.append(needle)
                    haystack.sort()

                    with open(temp_map_cycle, 'w') as map_cycle:
                        for line in haystack:
                            map_cycle.write(f"{line}\n")

                    uploader.upload(temp_map_cycle, server.map_cycle_location)
                    message_handler.add_sub_item_message(map_node, f"Inserted map into the mapcycle")

            if server.fast_download_server is not None and server.fast_download_server.id not in used_fast_dls:
                message_handler.add_sub_item_message(server_node, f"Uploading {compressed_base}")
                uploader.upload(compressed_path, remote_compressed_path)
                used_fast_dls.append(server.fast_download_server.id)

        except ConnectionFailure as ex:
            message_handler.add_sub_item_message(server_node, "Could not connect to the remote server -- Please contact an admin")
            log.exception = ex.base_error
            log.save()
            raise ex.base_error
        except AuthenticationFailure as ex:
            message_handler.add_sub_item_message(server_node, "Could not login to the remote server -- Please contact an Admin")
            log.exception = ex.base_error
            log.save()
            raise ex.base_error
        except TransmissionError as ex:
            message_handler.add_sub_item_message(server_node, "There was an error while transmitting the file -- Please contact an Admin")
            log.exception = ex.base_error
            log.save()
            raise ex.base_error

    if os.path.exists(file_path):
        os.remove(file_path)
    if os.path.exists(compressed_path):
        os.remove(compressed_path)

    log.success = True
    log.save()


@app.task(name="uploader.tasks.insert_map_information")
def insert_map_information(result, channel_name, database_id, map_name, map_author, map_type, map_tier,
                                                   map_zones, map_bonuses, disable_prehop, baked_triggers, map_spawns):
    message_handler = MessageHandler(channel_name)
    database = Database.objects.get(pk=database_id)

    try:

        new_map = Map.objects.using(database.dictionary_name).filter(name=map_name).first()

        if new_map is None:
            new_map = Map()

        new_map.active = 1
        new_map.name = map_name
        new_map.author = map_author
        new_map.mapType = map_type
        new_map.difficulty = map_tier
        new_map.checkpoints = map_zones
        new_map.bonuses = map_bonuses
        new_map.prehop = disable_prehop
        new_map.enableBakedTriggers = baked_triggers
        new_map.save(using=database.dictionary_name)

        message_handler.send_message("Successfully inserted map into the database")
    except IntegrityError as ex:
        message_handler.send_message("Failed to insert the map into the database")
    except Exception as ex:
        message_handler.send_message("Unhandled error occurred")




#@task_success.connect(sender=upload_map)
def upload_map_success(signal, sender, result, **kwargs):
    print("upload map success!")


#@task_failure.connect(sender=upload_map)
def upload_map_failure( **kwargs):
    print(kwargs)
    print("upload map failed!")

