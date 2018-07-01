from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

decorator_with_arguments = lambda decorator: lambda *args, **kwargs: lambda func: decorator(func, *args, **kwargs)


def has_uploader_permission(func):
    def _function(request, *args, **kwargs):
        uploader_permissions = [
            'uploader.uploader_access',
            'uploader.uploader_admin',
            'uploader.uploader_surf',
            'uploader.uploader_bhop',
        ]
        for perm in uploader_permissions:
            if request.user.has_perm(perm):
                return func(request, *args, **kwargs)

        # we did not find a valid permission
        return redirect('uploader:disabled')
    return _function