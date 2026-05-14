def user_roles(request):

    if not request.user.is_authenticated:

        return {

            'is_admin': False,
            'is_reception': False,
            'is_doctor': False,
            'is_lab': False,
            'is_dispense': False,

        }

    user = request.user

    return {

        'is_admin': user.is_superuser,

        'is_reception': user.groups.filter(
            name='Receptions'
        ).exists(),

        'is_doctor': user.groups.filter(
            name='Doctor'
        ).exists(),

        'is_lab': user.groups.filter(
            name='Lab'
        ).exists(),

        'is_dispense': user.groups.filter(
            name='Dispense'
        ).exists(),

    }