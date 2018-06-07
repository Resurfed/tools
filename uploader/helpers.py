import json
import tempfile
import os


def handle_uploaded_file(f):
    path = os.path.join(tempfile.gettempdir(), f.name)
    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return path


USER_CHANNEL_NAME = {

}