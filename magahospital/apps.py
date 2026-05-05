from django.apps import AppConfig


class MagahospitalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'magahospital'


class MagahospitalConfig(AppConfig):
    name = 'magahospital'

    def ready(self):
       # import magahospital.signals  # Replace 'magahospital' with your app name
       pass
