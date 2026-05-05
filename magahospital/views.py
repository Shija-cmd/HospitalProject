from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Patient, Visit, Doctor, Lab, Prescription, Dispense
from .forms import PatientForm, DoctorForm, LabForm, PrescriptionForm, DispenseForm
from django.db.models import Q
from functools import wraps

def group_required(group_name):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):

            # Not logged in
            if not request.user.is_authenticated:
                return HttpResponseForbidden("Login required")

            # Allowed users
            if request.user.is_superuser or request.user.groups.filter(name=group_name).exists():
                return view_func(request, *args, **kwargs)

            # Not allowed
            return HttpResponseForbidden("Not allowed")

        return _wrapped_view
    return decorator

# =========================
# AUTH VIEWS
# =========================

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'magahospital/register.html', {'form': form})


def index(request):
    return render(request, 'magahospital/index.html')

# =========================
# DASHBOARD (PRIVATE)
# =========================

@login_required
def dashboard(request):
    user = request.user

    context = {
        'is_doctor': user.groups.filter(name='Doctor').exists(),
        'is_lab': user.groups.filter(name='Lab').exists(),
        'is_dispense': user.groups.filter(name='Dispense').exists(),
        'is_admin': user.is_superuser,
    }

    return render(request, 'magahospital/dashboard.html', context)

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # IMPORTANT: redirect AFTER login
            return redirect('dashboard')

    else:
        form = AuthenticationForm()

    return render(request, 'magahospital/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


# =========================
# 1. PATIENT LIST
# =========================

@login_required
def patient_list(request):
    patients = Patient.objects.all().order_by('-created_at')

    # Search
    query = request.GET.get('q')
    if query:
        patients = patients.filter(
            Q(firstname__icontains=query) |
            Q(secondname__icontains=query) |
            Q(idno__icontains=query)
        )

    #Filter by sex
    sex = request.GET.get('sex')
    if sex:
        patients = patients.filter(sex=sex)

    return render(request, 'magahospital/patient_list.html', {
        'patients': patients
    })


# =========================
# 2. CREATE PATIENT (FORM)
# =========================

@login_required
def create_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patient_list')
    else:
        form = PatientForm()

    return render(request, 'magahospital/create_patient.html', {
        'form': form
    })


# =========================
# 3. CREATE VISIT
# =========================

@login_required
def create_visit(request, patient_id):
    patient = get_object_or_404(Patient, idno=patient_id)
    visit = Visit.objects.create(patient=patient)
    return redirect('visit_detail', visit_id=visit.id)


# =========================
# 4. VISIT DETAIL
# =========================

@login_required
def visit_detail(request, visit_id):
    visit = get_object_or_404(Visit, id=visit_id)

    doctor = getattr(visit, 'doctor', None)
    labs = visit.labs.all()
    prescriptions = visit.prescriptions.all()
    dispenses = visit.dispenses.all()

    return render(request, 'magahospital/visit_detail.html', {
        'visit': visit,
        'doctor': doctor,
        'labs': labs,
        'prescriptions': prescriptions,
        'dispenses': dispenses,
    })


# =========================
# 5. ADD / UPDATE DOCTOR (FORM)
# =========================

@login_required
@group_required('Doctor')
def add_doctor(request, visit_id):
    visit = get_object_or_404(Visit, id=visit_id)

    doctor, created = Doctor.objects.get_or_create(visit=visit)

    if request.method == 'POST':
        form = DoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            return redirect('visit_detail', visit_id=visit.id)
    else:
        form = DoctorForm(instance=doctor)

    return render(request, 'magahospital/doctor_form.html', {
        'form': form,
        'visit': visit
    })


# =========================
# 6. ADD LAB (FORM)
# =========================

@login_required
@group_required('Lab')
def add_lab(request, visit_id):
    visit = get_object_or_404(Visit, id=visit_id)

    if request.method == 'POST':
        form = LabForm(request.POST)
        if form.is_valid():
            lab = form.save(commit=False)
            lab.visit = visit
            lab.save()
            return redirect('visit_detail', visit_id=visit.id)
    else:
        form = LabForm()

    return render(request, 'magahospital/lab_form.html', {
        'form': form,
        'visit': visit
    })


# =========================
# 7. ADD PRESCRIPTION (FORM)
# =========================

@login_required
@group_required('Doctor')
def add_prescription(request, visit_id):
    visit = get_object_or_404(Visit, id=visit_id)

    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.visit = visit
            prescription.save()
            return redirect('visit_detail', visit_id=visit.id)
    else:
        form = PrescriptionForm()

    return render(request, 'magahospital/prescription_form.html', {
        'form': form,
        'visit': visit
    })


# =========================
# 8. ADD DISPENSE (FORM)
# =========================

@login_required
@group_required('Dispense')
def add_dispense(request, visit_id):
    visit = get_object_or_404(Visit, id=visit_id)

    if request.method == 'POST':
        form = DispenseForm(request.POST)
        if form.is_valid():
            dispense = form.save(commit=False)
            dispense.visit = visit
            dispense.save()
            return redirect('visit_detail', visit_id=visit.id)
    else:
        form = DispenseForm()

    return render(request, 'magahospital/dispense_form.html', {
        'form': form,
        'visit': visit
    })
    
    # =========================
# 9. PATIENT HISTORY
# =========================

@login_required
def patient_history(request, patient_id):
    patient = get_object_or_404(Patient, idno=patient_id)
    visits = patient.visits.all().order_by('-date')

    # Date filter
    start = request.GET.get('start')
    end = request.GET.get('end')

    if start:
        visits = visits.filter(date__gte=start)

    if end:
        visits = visits.filter(date__lte=end)

    return render(request, 'magahospital/patient_history.html', {
        'patient': patient,
        'visits': visits
    })  