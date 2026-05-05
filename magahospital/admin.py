from django.contrib import admin
from .models import Patient, Visit, Doctor, Lab, Prescription, Dispense

# Register your models here.

admin.site.register(Patient)
admin.site.register(Visit)
admin.site.register(Doctor)
admin.site.register(Lab)
admin.site.register(Prescription)
admin.site.register(Dispense)

admin.site.site_header = "Admin Panel"
admin.site.site_title = "Maga Hospital Admin"
admin.site.index_title = "Welcome to Maga Hospital Admin"