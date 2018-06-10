from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import UploadForm
from .helpers import handle_uploaded_file, USER_CHANNEL_NAME
from .tasks import process_map
import json
import time
# Create your views here.


@login_required
def uploader(request):

    if request.method == "POST":
        form = UploadForm(request.user, request.POST)

        if form.is_valid():
            insert_map_info = form.cleaned_data.get('insert_map_info')

            temp_file = None

            if 'map_file' not in request.FILES:
                return HttpResponse(json.dumps({"success": False, "error": "Missing map file"}),
                                    content_type='application/json')
            else:
                try:
                    temp_file = handle_uploaded_file(request.FILES['map_file'])

                except FileNotFoundError:
                    return HttpResponse(json.dumps({"success": False, "error": "Unable to save map file"}),
                                        content_type='application/json')

            if insert_map_info:
                pass

            servers = [server.id for server in form.cleaned_data.get('servers')]
            channel_name = USER_CHANNEL_NAME.get(request.user.id)
            process_map(channel_name, temp_file, servers, request.user.username)
            #print(f"We ran {task.id}")



        else:
            print("no!")

    return render(request, 'uploader.html', {
        'form': UploadForm(request.user)
    })