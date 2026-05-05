from django.contrib import admin
from .models import Receiption, Doctor_one, Lab, Med_Prescription, Dispense_Medics

# Register your models here.
admin.site.register(Receiption)
admin.site.register(Doctor_one)
admin.site.register(Lab)
admin.site.register(Med_Prescription)
admin.site.register(Dispense_Medics)

admin.site.site_header = "Admin Panel"
admin.site.site_title = "Maga Hospital Admin"
admin.site.index_title = "Welcome to Maga Hospital Admin"