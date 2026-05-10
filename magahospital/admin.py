from django.contrib import admin
from .models import Patient, Visit, Doctor, Lab, Prescription, Dispense
from .models import ChatMessage
from .models import ChatFAQ



# Register your models here.

admin.site.register(Patient)
admin.site.register(Visit)
admin.site.register(Doctor)
admin.site.register(Lab)
admin.site.register(Prescription)
admin.site.register(Dispense)
admin.site.register(ChatMessage)
admin.site.register(ChatFAQ)

admin.site.site_header = "Admin Panel"
admin.site.site_title = "Maga Hospital Admin"
admin.site.index_title = "Welcome to Maga Hospital Admin"