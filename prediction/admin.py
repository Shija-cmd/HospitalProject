from django.contrib import admin
from .models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):

    list_display = (
        'jina_la_kwanza',
        'jina_la_pili',
        'MAAMBUKIZI',
        'hospitali',
        'created'
    )

    readonly_fields = ('MAAMBUKIZI',)