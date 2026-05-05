from django.db import models
import random
import string
from django.utils import timezone


# Create your models here.
# -------------------------
# CONSTANTS
# -------------------------

SEX = [
    ('M', 'Male'),
    ('F', 'Female'),
]

LAB = [
    (1, 'LAB 1'),
    (2, 'LAB 2'),
    (3, 'LAB 3'),
    (4, 'LAB 4'),
    (5, 'LAB 5'),
]


# -------------------------
# HELPERS
# -------------------------

def generate_random_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))


# -------------------------
# MODELS
# -------------------------

# Patient (Reception)
class Patient(models.Model):
    idno = models.CharField(
        max_length=9,
        unique=True,
        default=generate_random_code,
        editable=False
    )
    firstname = models.CharField(max_length=200)
    secondname = models.CharField(max_length=200)
    age = models.IntegerField()
    address = models.CharField(max_length=200)
    sex = models.CharField(max_length=1, choices=SEX)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.idno} - {self.firstname} {self.secondname}"


# Visit (supports multiple visits per patient)
class Visit(models.Model):
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="visits"
    )
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.patient.idno} - {self.date}"


# Doctor (one per visit)
class Doctor(models.Model):
    visit = models.OneToOneField(
        Visit,
        on_delete=models.CASCADE,
        related_name="doctor"
    )
    history = models.TextField(blank=True, null=True)
    diagnosis = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Doctor - {self.visit}"


# Lab (multiple per visit)
class Lab(models.Model):
    visit = models.ForeignKey(
    Visit,
    on_delete=models.CASCADE,
    related_name='labs'
)
    lab_type = models.IntegerField(choices=LAB)
    results = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Lab {self.lab_type} - {self.visit}"


# Prescription (multiple per visit)
class Prescription(models.Model):
    visit = models.ForeignKey(
        Visit,
        on_delete=models.CASCADE,
        related_name="prescriptions"
    )
    medication = models.TextField()
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Prescription - {self.visit}"


# Dispense (multiple per visit)
class Dispense(models.Model):
    visit = models.ForeignKey(
        Visit,
        on_delete=models.CASCADE,
        related_name="dispenses"
    )
    medication_given = models.TextField()
    quantity = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Dispense - {self.visit}"