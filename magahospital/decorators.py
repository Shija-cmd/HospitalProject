from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from functools import wraps


def role_required(*group_names):

    def decorator(view_func):

        @login_required
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            if request.user.is_superuser:

                return view_func(
                    request,
                    *args,
                    **kwargs
                )

            if request.user.groups.filter(
                name__in=group_names
            ).exists():

                return view_func(
                    request,
                    *args,
                    **kwargs
                )

            return render(
                request,
                'magahospital/not_allowed.html',
                status=403
            )

        return wrapper

    return decorator