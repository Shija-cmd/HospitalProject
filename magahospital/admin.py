from django.contrib import admin
from .models import Patient, Visit, Doctor, Lab, Prescription, Dispense
from .models import ChatMessage
from .models import ChatFAQ
from .models import AuditLog
from .models import Bill
from .models import Vital
from .models import Procedure
from .models import MedicineStock
from .models import Appointment
from .models import Test
from .models import ProcedureCatalog
from .models import HospitalSettings



# Register your models here.

admin.site.register(Patient)
admin.site.register(Visit)
admin.site.register(Doctor)
admin.site.register(Lab)
admin.site.register(Prescription)
admin.site.register(Dispense)
admin.site.register(ChatMessage)
admin.site.register(ChatFAQ)
admin.site.register(AuditLog)
admin.site.register(Bill)
admin.site.register(Vital)
admin.site.register(Procedure)
admin.site.register(MedicineStock)
admin.site.register(Appointment)
admin.site.register(Test)
admin.site.register(ProcedureCatalog)

@admin.register(HospitalSettings)
class HospitalSettingsAdmin(admin.ModelAdmin):

    def has_add_permission(
        self,
        request
    ):
        return not HospitalSettings.objects.exists()

admin.site.site_header = "Admin Panel"
admin.site.site_title = "Maga Hospital Admin"
admin.site.index_title = "Welcome to Maga Hospital Admin"