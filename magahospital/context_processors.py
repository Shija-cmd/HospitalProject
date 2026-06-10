from .models import HospitalSettings

def user_roles(request):

    if not request.user.is_authenticated:

        return {

            'is_admin': False,

            'is_reception': False,

            'is_doctor': False,

            'is_lab': False,

            'is_cashier': False,

            'is_dispense': False,
            
            'is_vitals': False,

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

        'is_cashier': user.groups.filter(
            name='Cashier'
        ).exists(),

        'is_dispense': user.groups.filter(
            name='Dispense'
        ).exists(),
        
        'is_vitals': user.groups.filter(
            name='Vitals'
        ).exists(),

    }
    
def hospital_settings(request):

    settings = HospitalSettings.objects.first()

    return {
        'hospital_settings': settings
    }    