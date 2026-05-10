from django.urls import path
from .views import PatientCreate

urlpatterns = [
    path('predict/', PatientCreate.as_view(), name='predict'),
]