from django.db import models
import random
import string
from django.utils import timezone


# Create your models here.
SEX = [
    ('M', 'M'),
    ('F', 'F'),
]
def generate_random_code():
    while True:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))
        if not Lab.objects.filter(idno=code).exists():
            return code

LAB = [
    (1, 'LAB 1'),
    (2, 'LAB 2'),
    (3, 'LAB 3'),
    (4, 'LAB 4'),
    (5, 'LAB 5'),
]
class Receiption(models.Model):
    idno = models.CharField(max_length=9, default=generate_random_code, db_index=True, editable = False, primary_key= True)
    firstname = models.CharField(max_length=200, null = True)
    secondname = models.CharField(max_length=200, null = True)
    age = models.IntegerField(null = True)
    address = models.CharField(max_length=200, null = True)
    sex = models.CharField(choices=SEX)
    date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.idno}"
    
class Doctor_one(models.Model):
    idno = models.OneToOneField(Receiption, primary_key = True, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=200, null = True)
    secondname = models.CharField(max_length=200, null = True)
    age = models.IntegerField(null = True)
    address = models.CharField(max_length=200, null = True)
    sex = models.CharField(choices=SEX)
    date = models.DateTimeField(default=timezone.now)
    history = models.TextField(null=True, blank=True)
    lab_tests = models.TextField(null = True)
    
    def __str__(self):
        return f"{self.idno.idno} - {self.firstname} {self.secondname}"
    
class Lab(models.Model):
    idno = models.OneToOneField(Doctor_one, primary_key = True, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=200, null=True)
    secondname = models.CharField(max_length=200, null = True)
    age = models.IntegerField(null = True)
    address = models.CharField(max_length=200, null = True)
    sex = models.CharField(choices=SEX)
    date = models.DateTimeField(default=timezone.now)
    history = models.TextField(null=True, blank=True)
    lab_tests = models.TextField(null = True)
    lab_results = models.TextField(null = True)
    
    def __str__(self):
        return f"{self.idno.idno} - {self.firstname} {self.secondname}"
    
class Med_Prescription(models.Model):
    idno = models.OneToOneField(Lab, primary_key = True, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=200, null=True)
    secondname = models.CharField(max_length=200, null = True)
    age = models.IntegerField(null = True)
    address = models.CharField(max_length=200, null = True)
    sex = models.CharField(choices=SEX)
    date = models.DateTimeField(default=timezone.now)
    history = models.TextField(null=True, blank=True)
    lab_tests = models.TextField(null = True)
    lab_results = models.TextField(null = True)
    medical_prescription = models.TextField(null = True)
    
    def __str__(self):
        return f"{self.idno.idno}"
    
class Dispense_Medics(models.Model):
    idno = models.OneToOneField(Med_Prescription, primary_key = True, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=200, null=True)
    secondname = models.CharField(max_length=200, null = True)
    age = models.IntegerField(null = True)
    address = models.CharField(max_length=200, null = True)
    sex = models.CharField(choices=SEX)
    date = models.DateTimeField(default=timezone.now)
    history = models.TextField(null=True, blank=True)
    lab_tests = models.TextField(null = True)
    lab_results = models.TextField(null = True)
    medical_prescription = models.TextField(null = True)
    dispense_medication = models.TextField(null = True)
    
    def __str__(self):
        return f"{self.idno.idno}"