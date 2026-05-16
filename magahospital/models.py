from django.db import models
from django.utils import timezone
import random
import string
from django.contrib.auth.models import User


# =====================================
# CONSTANTS
# =====================================

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

VISIT_STATUS = [

    ('Doctor', 'Doctor'),
    ('Lab', 'Lab'),
    ('Prescription', 'Prescription'),
    ('Dispense', 'Dispense'),
    ('Completed', 'Completed'),

]


# =====================================
# HELPERS
# =====================================

def generate_random_code():
    return ''.join(
        random.choices(
            string.ascii_uppercase + string.digits,
            k=9
        )
    )


# =====================================
# PATIENT MODEL
# =====================================

class Patient(models.Model):

    idno = models.CharField(
        max_length=9,
        unique=True,
        default=generate_random_code,
        editable=False
    )

    firstname = models.CharField(
        max_length=200
    )

    secondname = models.CharField(
        max_length=200
    )

    age = models.IntegerField()

    address = models.CharField(
        max_length=200
    )

    sex = models.CharField(
        max_length=1,
        choices=SEX
    )

    created_at = models.DateTimeField(
        default=timezone.now
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.firstname} {self.secondname}"
        
@property
def current_visit(self):

    return Visit.objects.filter(
        patient=self
    ).order_by('-date').first()


# =====================================
# VISIT MODEL
# =====================================

class Visit(models.Model):

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='visits'
    )

    date = models.DateTimeField(
        default=timezone.now
    )

    # VISIT WORKFLOW STATUS
    status = models.CharField(
        max_length=20,
        choices=VISIT_STATUS,
        default='Doctor'
    )

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.patient} - {self.status}"


# =====================================
# DOCTOR MODEL
# ONE doctor record per visit
# =====================================

class Doctor(models.Model):

    visit = models.OneToOneField(
        Visit,
        on_delete=models.CASCADE,
        related_name='doctor'
    )

    history = models.TextField(
        blank=True,
        null=True
    )

    diagnosis = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        default=timezone.now
    )

    def __str__(self):
        return f"Doctor Record - Visit {self.visit.id}"


# =====================================
# LAB MODEL
# MANY labs per visit
# =====================================

class Lab(models.Model):

    visit = models.ForeignKey(
        Visit,
        on_delete=models.CASCADE,
        related_name='labs'
    )

    lab_type = models.IntegerField(
        choices=LAB
    )

    results = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        default=timezone.now
    )

    def __str__(self):
        return f"Lab {self.lab_type} - Visit {self.visit.id}"


# =====================================
# PRESCRIPTION MODEL
# MANY prescriptions per visit
# =====================================

class Prescription(models.Model):

    visit = models.ForeignKey(
        Visit,
        on_delete=models.CASCADE,
        related_name='prescriptions'
    )

    medication = models.CharField(
        max_length=255
    )

    notes = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        default=timezone.now
    )

    def __str__(self):
        return f"Prescription - Visit {self.visit.id}"


# =====================================
# DISPENSE MODEL
# MANY dispense records per visit
# =====================================

class Dispense(models.Model):

    visit = models.ForeignKey(
        Visit,
        on_delete=models.CASCADE,
        related_name='dispenses'
    )

    medication_given = models.CharField(
    max_length=255
)

    quantity = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        default=timezone.now
    )

    def __str__(self):
        return f"Dispense - Visit {self.visit.id}"
    
from django.db import models

#======================================
# CHAT MESSAGE MODEL
#======================================
class ChatMessage(models.Model):
    
    user = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    null=True,
    blank=True
    )

    user_message = models.TextField()

    bot_response = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_message[:50]
    
class ChatFAQ(models.Model):

    question = models.CharField(max_length=255)

    answer = models.TextField()

    def __str__(self):
        return self.question 
    
    from django.contrib.auth.models import User

#======================================
# AUDIT LOG MODEL
#======================================
class AuditLog(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    action = models.CharField(
        max_length=255
    )

    timestamp = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        if self.user:
            return f"{self.user.username} - {self.action}"

        return self.action   