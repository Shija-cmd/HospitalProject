from django.contrib import admin
from django.urls import path
from magahospital import views
from .views import chatbot_response
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from magahospital.sitemaps import StaticViewSitemap

sitemaps = {
    'static': StaticViewSitemap,
}

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
        'visit/create/<int:patient_id>/',
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
    # PROCEDURE
    # =========================

    path(
        'procedure/queue/',
        views.procedure_queue,
        name='procedure_queue'
    ),

    path(
        'add-procedure/<int:visit_id>/',
        views.add_procedure,
        name='add_procedure'
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
    
    #=========================
    # 7. STAFF MANAGEMENT
    #=========================
    
    #=========================
# STAFF MANAGEMENT
#=========================

    path(
        'staff-management/',
        views.staff_management,
        name='staff_management'
    ),

    path(
        'staff/toggle-status/<int:user_id>/',
        views.toggle_staff_status,
        name='toggle_staff_status'
    ),
    
    path(
        'staff/change-role/<int:user_id>/',
        views.change_staff_role,
        name='change_staff_role'
    ),
    
    #=========================
    # 8. CASHIER QUEUE
    #========================= 
    path(
        'cashier/',
        views.cashier_queue,
        name='cashier_queue'
    ),

    path(
        'bill/<int:visit_id>/',
        views.add_bill,
        name='add_bill'
    ),
    
    
    path(
        'vitals/',
        views.vital_queue,
        name='vital_queue'
    ),

    path(
        'add-vital/<int:visit_id>/',
        views.add_vital,
        name='add_vital'
    ),
    
    path(
        'add-procedure/<int:visit_id>/',
        views.add_procedure,
        name='add_procedure'
    ),
    
    path(
        'stock/',
        views.stock_list,
        name='stock_list'
    ),
    
    path(
        'stock/add/',
        views.add_stock,
        name='add_stock'
    ),
    
    path(
        'stock/edit/<int:stock_id>/',
        views.edit_stock,
        name='edit_stock'
    ),
    
    path(
        'stock/delete/<int:stock_id>/',
        views.delete_stock,
        name='delete_stock'
    ),
    
    path(
        'stock/adjust/<int:stock_id>/',
        views.adjust_stock,
        name='adjust_stock'
    ),
    
    path(
        'appointments/',
        views.appointment_list,
        name='appointment_list'
    ),

    path(
        'add-appointment/',
        views.add_appointment,
        name='add_appointment'
    ),
    
    path(
        'audit-logs/',
        views.audit_logs,
        name='audit_logs'
    ), 
    
    path(
        "robots.txt",
        TemplateView.as_view(
        template_name="magahospital/robots.txt",
        content_type="text/plain"
        ),
    ),
    
    path(
        'sitemap.xml',
        sitemap,
        {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'
    ),
    
    path(
        'change-password/',
        views.change_password,
        name='change_password'
    ),
    
    path(
        'hospital-settings/',
        views.hospital_settings,
        name='hospital_settings'
    ),
    
    path(
        'backup-database/',
        views.backup_database,
        name='backup_database'
    ),
    
    path(
        'backups/',
        views.backup_list,
        name='backup_list'
    ),
    
    path(
        'backups/download/<str:filename>/',
        views.download_backup,
        name='download_backup'
    ),
    
    path(
        'backups/delete/<str:filename>/',
        views.delete_backup,
        name='delete_backup'
    ),
    
    path(
        'backups/restore/',
        views.restore_backup,
        name='restore_backup'
    ),
    
    path(
        'invoice/<int:bill_id>/',
        views.invoice_pdf,
        name='invoice_pdf'
    ),

path(
    'receipt/<int:bill_id>/',
    views.receipt_pdf,
    name='receipt_pdf'
),

path(
    'payment-success/<int:bill_id>/',
    views.payment_success,
    name='payment_success'
),

path(
    'billing-history/',
    views.billing_history,
    name='billing_history'
),

path(
    'about/',
    views.about,
    name='about'
),

path(
    'services/',
    views.services,
    name='services'
),

path(
    'contact/',
    views.contact,
    name='contact'
),
]

# =========================
# GLOBAL HANDLER
# =========================

handler403 = 'magahospital.views.custom_403'

# =========================
# MEDIA FILES
# =========================
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)