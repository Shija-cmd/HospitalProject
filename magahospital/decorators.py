from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def role_required(group_name):

    def decorator(view_func):

        @login_required
        def wrapper(request, *args, **kwargs):

            if request.user.is_superuser:

                return view_func(
                    request,
                    *args,
                    **kwargs
                )

            if request.user.groups.filter(
                name=group_name
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