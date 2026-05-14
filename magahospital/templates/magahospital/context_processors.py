def user_roles(request):

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