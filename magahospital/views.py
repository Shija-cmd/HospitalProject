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

@login_required
def doctor_queue(request):

    if not (
        request.user.is_superuser or
        user_in_group(
            request.user,
            'Doctor'
        )
    ):

        return render(
            request,
            'magahospital/not_allowed.html',
            status=403
        )

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

@login_required
def lab_queue(request):

    if not (
        request.user.is_superuser or
        user_in_group(
            request.user,
            'Lab'
        )
    ):

        return render(
            request,
            'magahospital/not_allowed.html',
            status=403
        )

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

@login_required
def dispense_queue(request):

    if not (
        request.user.is_superuser or
        user_in_group(
            request.user,
            'Dispense'
        )
    ):

        return render(
            request,
            'magahospital/not_allowed.html',
            status=403
        )

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
# 1. PATIENT LIST
# =========================================

@login_required
def patient_list(request):

    query = request.GET.get('q')

    sex = request.GET.get('sex')

    patients = Patient.objects.prefetch_related(
        'visits'
    ).all().order_by(
        '-created_at'
    )

    # SEARCH
    if query:

        patients = patients.filter(

            Q(firstname__icontains=query) |
            Q(secondname__icontains=query) |
            Q(idno__icontains=query)

        )

    # FILTER SEX
    if sex:

        patients = patients.filter(
            sex=sex
        )

    # CONVERT TO LIST
    patients = list(patients)

    # ATTACH LATEST VISIT
    for patient in patients:

        patient.current_visit = Visit.objects.filter(
        patient=patient
    ).order_by('-id').first()

    return render(
        request,
        'magahospital/patient_list.html',
        {
            'patients': patients
        }
    )


# =========================================
# 2. CREATE PATIENT
# =========================================

@login_required
def create_patient(request):

    if not (
        request.user.is_superuser or
        user_in_group(
            request.user,
            'Receptions'
        )
    ):

        return render(
            request,
            'magahospital/not_allowed.html',
            status=403
        )

    if request.method == 'POST':

        form = PatientForm(request.POST)

        if form.is_valid():

            form.save()

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
# 3. CREATE NEW VISIT
# =========================================

@login_required
def create_visit(request, patient_id):

    if not (
        request.user.is_superuser or
        user_in_group(
            request.user,
            'Receptions'
        )
    ):

        return render(
            request,
            'magahospital/not_allowed.html',
            status=403
        )

    patient = get_object_or_404(
        Patient,
        idno=patient_id
    )

    visit = Visit.objects.create(
        patient=patient,
        status='Doctor'
    )

    return redirect(
        'visit_detail',
        visit_id=visit.id
    )


# =========================================
# 4. VISIT DETAIL
# =========================================

@login_required
def visit_detail(request, visit_id):

    visit = get_object_or_404(
        Visit,
        id=visit_id
    )

    doctor = getattr(
        visit,
        'doctor',
        None
    )

    labs = visit.labs.all()

    prescriptions = visit.prescriptions.all()

    dispenses = visit.dispenses.all()

    return render(
        request,
        'magahospital/visit_detail.html',
        {
            'visit': visit,
            'doctor': doctor,
            'labs': labs,
            'prescriptions': prescriptions,
            'dispenses': dispenses,
        }
    )


# =========================================
# 5. ADD / UPDATE DOCTOR
# =========================================

@login_required
def add_doctor(request, visit_id):

    if not (
        request.user.is_superuser or
        user_in_group(
            request.user,
            'Doctor'
        )
    ):

        return render(
            request,
            'magahospital/not_allowed.html',
            status=403
        )

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
# 6. ADD LAB
# =========================================

@login_required
def add_lab(request, visit_id):

    if not (
        request.user.is_superuser or
        user_in_group(
            request.user,
            'Lab'
        )
    ):

        return render(
            request,
            'magahospital/not_allowed.html',
            status=403
        )

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
# 7. ADD PRESCRIPTION
# =========================================

@login_required
def add_prescription(request, visit_id):

    if not (
        request.user.is_superuser or
        user_in_group(
            request.user,
            'Doctor'
        )
    ):

        return render(
            request,
            'magahospital/not_allowed.html',
            status=403
        )

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
# 8. ADD DISPENSE
# =========================================

@login_required
def add_dispense(request, visit_id):

    if not (
        request.user.is_superuser or
        user_in_group(
            request.user,
            'Dispense'
        )
    ):

        return render(
            request,
            'magahospital/not_allowed.html',
            status=403
        )

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
# 9. PATIENT HISTORY
# =========================================

@login_required
def patient_history(request, patient_id):

    patient = get_object_or_404(
        Patient,
        idno=patient_id
    )

    visits = patient.visits.all().order_by(
        '-date'
    )

    start = request.GET.get('start')

    end = request.GET.get('end')

    if start:

        visits = visits.filter(
            date__gte=start
        )

    if end:

        visits = visits.filter(
            date__lte=end
        )

    return render(
        request,
        'magahospital/patient_history.html',
        {
            'patient': patient,
            'visits': visits
        }
    )


# =========================================
# GLOBAL 403 HANDLER
# =========================================

def custom_403(request, exception):

    return render(
        request,
        'magahospital/not_allowed.html',
        status=403
    )
    
    # =========================================
# PDF VISIT REPORT
# =========================================

@login_required
def visit_report_pdf(request, visit_id):

    visit = get_object_or_404(
        Visit,
        id=visit_id
    )

    doctor = getattr(
        visit,
        'doctor',
        None
    )

    labs = visit.labs.all()

    prescriptions = visit.prescriptions.all()

    dispenses = visit.dispenses.all()

    template_path = 'magahospital/visit_report_pdf.html'

    context = {

        'visit': visit,
        'doctor': doctor,
        'labs': labs,
        'prescriptions': prescriptions,
        'dispenses': dispenses,

    }

    response = HttpResponse(
        content_type='application/pdf'
    )

    response[
        'Content-Disposition'
    ] = f'filename="visit_{visit.id}.pdf"'

    template = get_template(
        template_path
    )

    html = template.render(
        context
    )

    pisa_status = pisa.CreatePDF(
        html,
        dest=response
    )

    if pisa_status.err:

        return HttpResponse(
            'PDF generation error'
        )

    return response

# =========================================
# CHATBOT RESPONSE
# =========================================

def chatbot_response(request):

    if request.method == "POST":

        try:

            data = json.loads(request.body)

            user_message = data.get("message", "")

            message = user_message.lower()

            faq = None

            for item in ChatFAQ.objects.all():

                if item.question.lower() in message:

                    faq = item

                    break

            if faq:

                bot_reply = faq.answer

            else:

                bot_reply = "Sorry, I could not find an answer to your question."

            time.sleep(1.5)

            # SAVE CHAT SAFELY
            try:

                ChatMessage.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    user_message=user_message,
                    bot_response=bot_reply
                )

            except Exception as db_error:

                print("Chat save error:", db_error)

            return JsonResponse({
                "response": bot_reply
            })

        except Exception as e:

            print("Chatbot error:", e)

            return JsonResponse({
                "response": f"Server Error: {str(e)}"
            })

    return JsonResponse({
        "response": "Invalid request"
    })
    
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
