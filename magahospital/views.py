from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse
from .models import ChatMessage
from .models import ChatFAQ
import time
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
from django.contrib import messages

from .models import (
    Patient,
    Visit,
    Doctor,
    Lab,
    Prescription,
    Dispense
)

from .forms import (
    PatientForm,
    DoctorForm,
    LabForm,
    PrescriptionForm,
    DispenseForm
)

from django.http import JsonResponse
import json
from .models import AuditLog
from .decorators import role_required

# =========================================
# GROUP HELPER
# =========================================

def user_in_group(user, group_name):

    return user.groups.filter(
        name=group_name
    ).exists()


# =========================================
# AUTH VIEWS
# =========================================


def index(request):

    return render(
        request,
        'magahospital/index.html'
    )


def login_view(request):

    if request.method == 'POST':

        form = AuthenticationForm(
            request,
            data=request.POST
        )

        if form.is_valid():

            user = form.get_user()

            login(request, user)

            return redirect('dashboard')

    else:

        form = AuthenticationForm()

    return render(
        request,
        'magahospital/login.html',
        {'form': form}
    )


def logout_view(request):

    logout(request)

    return redirect('login')


# =========================================
# DASHBOARD
# =========================================

@login_required
def dashboard(request):

    user = request.user

    context = {

        # USER ROLES
        'is_admin': user.is_superuser,

        'is_reception': user_in_group(
            user,
            'Receptions'
        ),

        'is_doctor': user_in_group(
            user,
            'Doctor'
        ),

        'is_lab': user_in_group(
            user,
            'Lab'
        ),

        'is_dispense': user_in_group(
            user,
            'Dispense'
        ),

        # DASHBOARD STATISTICS
        'total_patients': Patient.objects.count(),

        'doctor_waiting': Visit.objects.filter(
            status='Doctor'
        ).count(),

        'lab_waiting': Visit.objects.filter(
            status='Lab'
        ).count(),

        'prescription_waiting': Visit.objects.filter(
            status='Prescription'
        ).count(),

        'dispense_waiting': Visit.objects.filter(
            status='Dispense'
        ).count(),

        'completed_visits': Visit.objects.filter(
            status='Completed'
        ).count(),

    }

    return render(
        request,
        'magahospital/dashboard.html',
        context
    )


# =========================================
# DOCTOR QUEUE
# =========================================

@role_required('Doctor')
def doctor_queue(request):

    visits = Visit.objects.filter(
        status__in=[
            'Doctor',
            'Prescription'
        ]
    ).order_by('-date')

    return render(
        request,
        'magahospital/doctor_queue.html',
        {
            'visits': visits
        }
    )


# =========================================
# LAB QUEUE
# =========================================

@role_required('Lab')
def lab_queue(request):

    visits = Visit.objects.filter(
        status='Lab'
    ).order_by('-date')

    return render(
        request,
        'magahospital/lab_queue.html',
        {
            'visits': visits
        }
    )


# =========================================
# DISPENSE QUEUE
# =========================================

@role_required('Dispense')
def dispense_queue(request):

    visits = Visit.objects.filter(
        status='Dispense'
    ).order_by('-date')

    return render(
        request,
        'magahospital/dispense_queue.html',
        {
            'visits': visits
        }
    )


# =========================================
# CREATE PATIENT
# =========================================

@role_required('Receptions')
def create_patient(request):

    if request.method == 'POST':

        form = PatientForm(request.POST)

        if form.is_valid():

            patient = form.save()

            log_action(
                request.user,
                f"Created patient {patient.firstname} {patient.secondname}"
            )

            return redirect('patient_list')

    else:

        form = PatientForm()

    return render(
        request,
        'magahospital/create_patient.html',
        {
            'form': form
        }
    )


# =========================================
# CREATE VISIT
# =========================================

@role_required('Receptions')
def create_visit(request, patient_id):

    patient = get_object_or_404(
        Patient,
        idno=patient_id
    )

    visit = Visit.objects.create(
        patient=patient,
        status='Doctor'
    )

    log_action(
        request.user,
        f"Created visit for patient {patient.firstname} {patient.secondname}"
    )

    return redirect(
        'visit_detail',
        visit_id=visit.id
    )


# =========================================
# ADD DOCTOR
# =========================================

@role_required('Doctor')
def add_doctor(request, visit_id):

    visit = get_object_or_404(
        Visit,
        id=visit_id
    )

    doctor, created = Doctor.objects.get_or_create(
        visit=visit
    )

    if request.method == 'POST':

        form = DoctorForm(
            request.POST,
            instance=doctor
        )

        if form.is_valid():

            doctor = form.save(
                commit=False
            )

            doctor.visit = visit

            doctor.save()

            log_action(
                request.user,
                f"Added doctor consultation for Visit #{visit.id}"
            )

            visit.status = 'Lab'

            visit.save()

            return redirect(
                'doctor_queue'
            )

    else:

        form = DoctorForm(
            instance=doctor
        )

    return render(
        request,
        'magahospital/doctor_form.html',
        {
            'form': form,
            'visit': visit
        }
    )


# =========================================
# ADD LAB
# =========================================

@role_required('Lab')
def add_lab(request, visit_id):

    visit = get_object_or_404(
        Visit,
        id=visit_id
    )

    if request.method == 'POST':

        form = LabForm(request.POST)

        if form.is_valid():

            lab = form.save(
                commit=False
            )

            lab.visit = visit

            lab.save()

            log_action(
                request.user,
                f"Added lab results for Visit #{visit.id}"
            )

            visit.status = 'Prescription'

            visit.save()

            return redirect(
                'lab_queue'
            )

    else:

        form = LabForm()

    return render(
        request,
        'magahospital/lab_form.html',
        {
            'form': form,
            'visit': visit
        }
    )


# =========================================
# ADD PRESCRIPTION
# =========================================

@role_required('Doctor')
def add_prescription(request, visit_id):

    visit = get_object_or_404(
        Visit,
        id=visit_id
    )

    if request.method == 'POST':

        form = PrescriptionForm(
            request.POST
        )

        if form.is_valid():

            prescription = form.save(
                commit=False
            )

            prescription.visit = visit

            prescription.save()

            log_action(
                request.user,
                f"Added prescription for Visit #{visit.id}"
            )

            visit.status = 'Dispense'
            visit.save()

            return redirect(
                'visit_detail',
                visit_id=visit.id
            )

    else:

        form = PrescriptionForm()

    return render(
        request,
        'magahospital/prescription_form.html',
        {
            'form': form,
            'visit': visit
        }
    )


# =========================================
# ADD DISPENSE
# =========================================

@role_required('Dispense')
def add_dispense(request, visit_id):

    visit = get_object_or_404(
        Visit,
        id=visit_id
    )

    if request.method == 'POST':

        form = DispenseForm(
            request.POST
        )

        if form.is_valid():

            dispense = form.save(
                commit=False
            )

            dispense.visit = visit

            dispense.save()

            log_action(
                request.user,
                f"Dispensed medication for Visit #{visit.id}"
            )

            visit.status = 'Completed'

            visit.save()

            return redirect(
                'dispense_queue'
            )

    else:

        form = DispenseForm()

    return render(
        request,
        'magahospital/dispense_form.html',
        {
            'form': form,
            'visit': visit
        }
    )


# =========================================
# STAFF MANAGEMENT
# =========================================

@login_required
def staff_management(request):

    if not request.user.is_superuser:

        return render(
            request,
            'magahospital/not_allowed.html',
            status=403
        )

    users = User.objects.all().order_by('-id')

    groups = Group.objects.all()

    if request.method == 'POST':

        username = request.POST.get('username')

        password = request.POST.get('password')

        group_name = request.POST.get('group')

        if User.objects.filter(username=username).exists():

            messages.error(
                request,
                'Username already exists.'
            )

            return redirect('staff_management')

        user = User.objects.create(
            username=username,
            password=make_password(password)
        )

        group = Group.objects.get(name=group_name)

        user.groups.add(group)

        messages.success(
            request,
            f'Staff account for {username} created successfully.'
        )

        return redirect('staff_management')

    return render(
        request,
        'magahospital/staff_management.html',
        {
            'users': users,
            'groups': groups
        }
    )

#=========================================
# AUDIT LOG
#=========================================
def log_action(user, action):

    AuditLog.objects.create(

        user=user,

        action=action

    )
    
    # =========================================
# CHATBOT RESPONSE
# =========================================

def chatbot_response(request):

    if request.method == 'POST':

        data = json.loads(request.body)

        user_message = data.get(
            'message',
            ''
        ).strip()

        ChatMessage.objects.create(
            user_message=user_message
        )

        faqs = ChatFAQ.objects.all()

        response = (
            "Sorry, I could not find an answer "
            "to your question."
        )

        for faq in faqs:

            if faq.question.lower() in user_message.lower():

                response = faq.answer

                break

        return JsonResponse({
            'response': response
        })

    return JsonResponse({
        'response': 'Invalid request'
    })