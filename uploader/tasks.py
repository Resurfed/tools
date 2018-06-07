from tools.celery import app
from .models import Server
from .choices import ServerType


@app.task(name="uploader.upload_map")
def upload_map(channel_name, file_path, servers):
    print("Hello we are run")