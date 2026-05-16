from django import forms
from .models import Patient


class PredictionForm(forms.ModelForm):

    class Meta:

        model = Patient

        fields = [

            'umri',
            'jinsia',
            'DALILI1',
            'DALILI2',
            'DALILI3',
            'DALILI4',
            'DALILI5',

        ]

        widgets = {

            'umri': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter age'
                }
            ),

            'jinsia': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'DALILI1': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'DALILI2': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'DALILI3': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'DALILI4': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'DALILI5': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

        }