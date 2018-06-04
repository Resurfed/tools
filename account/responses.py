import json

from django.http import HttpResponse


def ajax_response(success, status=200, **kwargs):

    data = {
        'success': success
    }
    data.update(**kwargs)

    return HttpResponse(json.dumps(data), content_type='application/json', status=status)