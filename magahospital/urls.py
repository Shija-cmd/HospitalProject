from django.contrib import admin
from django.urls import path
from magahospital import views
from .views import chatbot_response


urlpatterns = [

    # =========================
    # AUTH + HOME
    # =========================

    path(
        '',
        views.index,
        name='index'
    ),

    path(
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),

    path(
        'register/',
        views.register,
        name='register'
    ),

    path(
        'login/',
        views.login_view,
        name='login'
    ),

    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),

    path(
        'patient/<str:patient_id>/history/',
        views.patient_history,
        name='patient_history'
    ),
    
    path(
        'visit/<int:visit_id>/pdf/',
        views.visit_report_pdf,
        name='visit_report_pdf'
    ),


    # =========================
    # 1. PATIENTS
    # =========================

    path(
        'patients/',
        views.patient_list,
        name='patient_list'
    ),

    path(
        'patients/create/',
        views.create_patient,
        name='create_patient'
    ),


    # =========================
    # 2. VISITS
    # =========================

    path(
        'visit/create/<str:patient_id>/',
        views.create_visit,
        name='create_visit'
    ),

    path(
        'visit/<int:visit_id>/',
        views.visit_detail,
        name='visit_detail'
    ),


    # =========================
    # 3. DOCTOR
    # =========================

    path(
        'doctor/queue/',
        views.doctor_queue,
        name='doctor_queue'
    ),

    path(
        'doctor/<int:visit_id>/',
        views.add_doctor,
        name='add_doctor'
    ),


    # =========================
    # 4. LAB
    # =========================

    path(
        'lab/queue/',
        views.lab_queue,
        name='lab_queue'
    ),

    path(
        'lab/<int:visit_id>/',
        views.add_lab,
        name='add_lab'
    ),


    # =========================
    # 5. PRESCRIPTION
    # =========================

    path(
        'prescription/<int:visit_id>/',
        views.add_prescription,
        name='add_prescription'
    ),


    # =========================
    # 6. DISPENSE
    # =========================

    path(
        'dispense/queue/',
        views.dispense_queue,
        name='dispense_queue'
    ),

    path(
        'dispense/<int:visit_id>/',
        views.add_dispense,
        name='add_dispense'
    ),
    
    path(
        'chatbot/', chatbot_response, 
        name='chatbot'),
]




# =========================
# GLOBAL HANDLER
# =========================

handler403 = 'magahospital.views.custom_403'