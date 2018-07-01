from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from account.responses import ajax_response
from .forms import UploadForm
from .helpers import handle_uploaded_file
from .choices import DatabaseType
from . import tasks
import os
from os.path import splitext
import json
from celery import chain
from .models import Map
from home.decorators import has_uploader_permission
from django.conf import settings
# Create your views here.


@login_required
@has_uploader_permission
def uploader(request):

    if request.method == "POST":
        form = UploadForm(request.user, request.POST)

        if form.is_valid():
            insert_map_info = form.cleaned_data.get('insert_map_info')

            if 'map_file' not in request.FILES:
                return HttpResponse(json.dumps({"success": False, "error": "Missing map file"}),
                                    content_type='application/json')
            else:
                try:
                    temp_file = handle_uploaded_file(request.FILES['map_file'])

                except FileNotFoundError:
                    return HttpResponse(json.dumps({"success": False, "error": "Unable to save map file"}),
                                        content_type='application/json')

            servers = [server.id for server in form.cleaned_data.get('servers')]
            channel_name = form.data.get('channel_name')

            if insert_map_info:
                database_to_insert = form.cleaned_data.get('database')

                if database_to_insert in settings.DATABASES:
                    if database_to_insert.type == DatabaseType.Private:
                        if not request.user.has_perm('uploader.uploader_admin'):
                            return HttpResponse(json.dumps({"success": False, "error": "You do not have permission to upload to this database"}),
                                                content_type='application/json')

                map_author = form.cleaned_data.get('map_author')
                map_type = form.cleaned_data.get('map_type')
                map_tier = form.cleaned_data.get('map_tier')
                map_zones = form.cleaned_data.get('map_zones')
                map_bonuses = form.cleaned_data.get('map_bonuses')
                disable_prehop = form.cleaned_data.get('map_disable_pre_hop')
                baked_triggers = form.cleaned_data.get('map_enable_baked_triggers')
                map_spawns = form.cleaned_data.get('map_spawns')

                map_name = splitext(os.path.basename(temp_file))[0]

                chain(
                    tasks.process_map.s(channel_name, temp_file, servers, request.user.id),
                    tasks.insert_map_information.s(channel_name, database_to_insert.id, map_name, map_author,
                                                   map_type, map_tier, map_zones, map_bonuses, disable_prehop,
                                                   baked_triggers, map_spawns)
                ).apply_async()
            else:
                    tasks.process_map.delay(channel_name, temp_file, servers, request.user.id)

            return ajax_response(True)
        else:
            errors = []
            for item in form.errors:
                errors = [err for err in form.errors[item]]

            return ajax_response(False, 400, errors=errors)

    return render(request, 'uploader.html', {
        'form': UploadForm(request.user)
    })


def disabled(request):
    return HttpResponse("Sorry you are not authorized to view this page. "
                        "Please contact an Admin on discord to gain access. Click "
                        "<a href=\"https://discord.gg/0tr8WX4USWfzSjxQ\"> here </a> to join!")