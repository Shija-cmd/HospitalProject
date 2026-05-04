from django.contrib import admin
from .models import Receiption, Doctor_one, Lab, Med_Prescription, Dispense_Medics

# Register your models here.
admin.site.register(Receiption)
admin.site.register(Doctor_one)
admin.site.register(Lab)
admin.site.register(Med_Prescription)
admin.site.register(Dispense_Medics)