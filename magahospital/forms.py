from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Patient, Doctor, Lab, Prescription, Dispense


# =========================
# AUTH FORMS
# =========================

class CustomLoginForm(AuthenticationForm):

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter username'
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
    )


class CustomRegisterForm(UserCreationForm):

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter username'
        })
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


# =========================
# 1. PATIENT FORM
# =========================

class PatientForm(forms.ModelForm):

    class Meta:
        model = Patient
        fields = ['firstname', 'secondname', 'age', 'address', 'sex']

        widgets = {

            'firstname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter first name'
            }),

            'secondname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter second name'
            }),

            'age': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter age'
            }),

            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter address'
            }),

            'sex': forms.Select(attrs={
                'class': 'form-select'
            }),

        }


# =========================
# 2. DOCTOR FORM
# =========================

class DoctorForm(forms.ModelForm):

    class Meta:
        model = Doctor
        fields = ['history', 'diagnosis']

        widgets = {

            'history': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Enter patient history...'
            }),

            'diagnosis': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter diagnosis details...'
            }),

        }


# =========================
# 3. LAB FORM
# =========================

class LabForm(forms.ModelForm):

    class Meta:
        model = Lab
        fields = ['lab_type', 'results']

        widgets = {

            'lab_type': forms.Select(attrs={
                'class': 'form-select'
            }),

            'results': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter laboratory results...'
            }),

        }


# =========================
# 4. PRESCRIPTION FORM
# =========================

class PrescriptionForm(forms.ModelForm):

    class Meta:
        model = Prescription
        fields = ['medication', 'notes']

        widgets = {

            'medication': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter medication'
            }),

            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Additional prescription notes...'
            }),

        }

# =========================================
# DISPENSE FORM
# =========================================

class DispenseForm(forms.ModelForm):

    class Meta:

        model = Dispense

        fields = [
            'medication_given',
            'quantity'
        ]

        labels = {

            'medication_given': 'Medication Given',

            'quantity': 'Dosage Instructions'

        }

#=========================================
#Widgets for create_patient from .forms import 
#=========================================
        widgets = {

            'medication_given': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': (
                        'Example:\n'
                        'Panadol\n'
                        'Azithromycin\n'
                        'Vitamin C'
                    )
                }
            ),

            'quantity': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': (
                        'Example: 2*3/7 or '
                        '1 tablet OD for 5 days'
                    )
                }
            ),

        }
        
        widgets = {

    'firstname': forms.TextInput(
        attrs={'class': 'form-control'}
    ),

    'secondname': forms.TextInput(
        attrs={'class': 'form-control'}
    ),

    'age': forms.NumberInput(
        attrs={'class': 'form-control'}
    ),

    'sex': forms.Select(
        attrs={'class': 'form-select'}
    ),

    'address': forms.Textarea(
        attrs={
            'class': 'form-control',
            'rows': 3
        }
    ),

}
        
#=========================================
#Widgets for create_doctor from         
#=========================================
widgets = {

    'history': forms.Textarea(
        attrs={
            'class': 'form-control',
            'rows': 4
        }
    ),

    'diagnosis': forms.Textarea(
        attrs={
            'class': 'form-control',
            'rows': 4
        }
    ),

}

#=========================================
#Widgets for dispense_form from 
#=========================================
widgets = {

    'medication_given': forms.Textarea(
        attrs={
            'class': 'form-control',
            'rows': 3
        }
    ),

    'quantity': forms.TextInput(
        attrs={
            'class': 'form-control'
        }
    ),

}

#=========================================
#Widgets for prescription_form from 
#=========================================

widgets = {

    'medication': forms.Textarea(
        attrs={
            'class': 'form-control',
            'rows': 3
        }
    ),

    'notes': forms.Textarea(
        attrs={
            'class': 'form-control',
            'rows': 3
        }
    ),

}

#=========================================
#Widgets for lab_form from .forms import 
#=========================================
widgets = {

    'lab_type': forms.Select(
        attrs={
            'class': 'form-select'
        }
    ),

    'results': forms.Textarea(
        attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Enter laboratory results'
        }
    ),

}