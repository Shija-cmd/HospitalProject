from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Patient, Doctor, Lab, Prescription, Dispense


# =========================
# AUTH FORMS
# =========================

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )


class CustomRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


# =========================
# 1. PATIENT FORM
# =========================

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['firstname', 'secondname', 'age', 'address', 'sex']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


# =========================
# 2. DOCTOR FORM
# =========================

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['history', 'diagnosis']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


# =========================
# 3. LAB FORM
# =========================

class LabForm(forms.ModelForm):
    class Meta:
        model = Lab
        fields = ['lab_type', 'results']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


# =========================
# 4. PRESCRIPTION FORM
# =========================

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['medication', 'notes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


# =========================
# 5. DISPENSE FORM
# =========================

class DispenseForm(forms.ModelForm):
    class Meta:
        model = Dispense
        fields = ['medication_given', 'quantity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'