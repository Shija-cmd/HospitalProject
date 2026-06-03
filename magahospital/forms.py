from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Patient, Doctor, Lab, Prescription, Dispense, Bill, Vital, Procedure, MedicineStock, Appointment, Test


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

    tests = forms.ModelMultipleChoiceField(

        queryset=Test.objects.all(),

        required=False,

        widget=forms.CheckboxSelectMultiple()

    )

    class Meta:

        model = Doctor

        fields = [

            'history',

            'diagnosis',

            'tests',

            'next_step',

        ]

        labels = {

            'history': 'Patient History',

            'diagnosis': 'Diagnosis',

            'tests': 'Requested Tests',

            'next_step': 'Send Patient To'

        }

        widgets = {

            'history': forms.Textarea(
                attrs={
                    'class':'form-control',
                    'rows':5
                }
            ),

            'diagnosis': forms.Textarea(
                attrs={
                    'class':'form-control',
                    'rows':4
                }
            ),

            'next_step': forms.Select(
                attrs={
                    'class':'form-select'
                }
            ),

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
        fields = [

    'medication',

    'notes'

]

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
        
# =========================
# 5. BILL FORM
# =========================        
class BillForm(forms.ModelForm):

    class Meta:

        model = Bill

        fields = [

            'consultation_fee',

            'lab_fee',

            'medication_fee',
            
            'procedure_fee',

            'is_paid'

        ]

        labels = {

            'consultation_fee': 'Consultation Fee',

            'lab_fee': 'Laboratory Fee',

            'medication_fee': 'Medication Fee',

            'is_paid': 'Payment Completed'

        }

        widgets = {

            'consultation_fee': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Consultation fee'
                }
            ),

            'lab_fee': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Laboratory fee'
                }
        ),

            'medication_fee': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Medication fee'
                }
        ),

            'procedure_fee': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Procedure fee'
                }
        ),

            'is_paid': forms.CheckboxInput(
                attrs={
                'class': 'form-check-input'
                }
        ),

    }        

# =========================================
# DISPENSE FORM
# =========================================

class DispenseForm(forms.ModelForm):

    class Meta:

        model = Dispense

        fields = [
            'medication_given',
            'quantity',
            'dispensed_quantity'
        ]

        widgets = {

            'medication_given': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'quantity': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':
                    'e.g. 2×3 after meals'
                }
            ),

            'dispensed_quantity':
            forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':
                    'Number of tablets/capsules'
                }
            ),

        }

        def __init__(
            self,
            *args,
            **kwargs
            ):

            super().__init__(
                *args,
                **kwargs
            )

            self.fields[
                'medication_given'
            ].required = False

            self.fields[
                'quantity'
            ].required = False

            self.fields[
                'dispensed_quantity'
            ].required = False

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

#=========================================
#VITAL FORM
#=========================================

class VitalForm(forms.ModelForm):

    class Meta:

        model = Vital

        fields = [

            'blood_pressure',

            'temperature',

            'pulse_rate',

            'oxygen_saturation',

            'respiratory_rate',

            'weight',

            'height',

            'notes'

        ]

        widgets = {

            'blood_pressure': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '120/80'
                }
            ),

            'temperature': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '36.5'
                }
            ),

            'pulse_rate': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '72'
                }
            ),

            'oxygen_saturation': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '98'
                }
            ),

            'respiratory_rate': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '16'
                }
            ),

            'weight': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '70'
                }
            ),

            'height': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '170'
                }
            ),

            'notes': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Additional notes'
                }
            ),

        }
#=========================================
#PROCEDURE FORM
#=========================================        
class ProcedureForm(forms.ModelForm):

    class Meta:

        model = Procedure

        fields = [
            'procedure_name',
            'notes',
            'image',
        ]

        widgets = {

            'procedure_name': forms.Select(attrs={
                'class': 'form-select'
            }),

            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter procedure notes...'
            }),

            'cost': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter procedure cost'
            }),

        }

#=========================================
#MEDICINE STOCK FORM
#=========================================        
class MedicineStockForm(forms.ModelForm):

    class Meta:

        model = MedicineStock

        fields = [
            'medicine_name',
            'quantity',
            'unit_price',
            'expiry_date',
            'batch_number',
            'low_stock_alert'
        ]

        widgets = {

            'medicine_name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'quantity': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'unit_price': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'expiry_date': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            ),

            'batch_number': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'low_stock_alert': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),

        }   
        
#=========================================
#APPOINTMENT FORM
#=========================================
class AppointmentForm(forms.ModelForm):

    class Meta:

        model = Appointment

        fields = [

            'patient',

            'appointment_date',

            'appointment_time',

            'reason'

        ]

        widgets = {

            'patient': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'appointment_date': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            ),

            'appointment_time': forms.TimeInput(
                attrs={
                    'class': 'form-control',
                    'type': 'time'
                }
            ),

            'reason': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Appointment reason'
                }
            ),

        }             