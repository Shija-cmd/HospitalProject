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

    ('Waiting Vital', 'Waiting Vital'),

    ('Waiting Doctor', 'Waiting Doctor'),

    ('Waiting Lab', 'Waiting Lab'),

    ('Waiting Procedure', 'Waiting Procedure'),

    ('Doctor Review', 'Doctor Review'),

    ('Waiting Cashier', 'Waiting Cashier'),

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
        default='Waiting Vital'
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

    doctor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    history = models.TextField(
        blank=True,
        null=True
    )

    diagnosis = models.TextField(
        blank=True,
        null=True
    )
    
    tests = models.ManyToManyField(
        'Test',
        blank=True
    )

    
    NEXT_STEP_CHOICES = [

        ('Lab', 'Send To Laboratory'),

        ('Procedure', 'Send To Procedure'),

        ('Cashier', 'Send To Cashier'),

    ]

    next_step = models.CharField(
        max_length=20,
        choices=NEXT_STEP_CHOICES
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
# BILLING MODEL
# =====================================

class Bill(models.Model):

    visit = models.OneToOneField(
        Visit,
        on_delete=models.CASCADE,
        related_name='bill'
    )

    consultation_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    lab_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    medication_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    
    procedure_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    is_paid = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        default=timezone.now
    )

    def save(self, *args, **kwargs):

        self.total_amount = (

            self.consultation_fee +

            self.lab_fee +

            self.medication_fee +

            self.procedure_fee

    )

        super().save(*args, **kwargs)

    def __str__(self):

        return f"Bill - Visit {self.visit.id}"    

# =====================================
# PHARMACY STOCK
# =====================================

class MedicineStock(models.Model):

    medicine_name = models.CharField(
        max_length=200
    )

    quantity = models.PositiveIntegerField(
        default=0
    )

    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    expiry_date = models.DateField()

    batch_number = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    low_stock_alert = models.PositiveIntegerField(
        default=10
    )

    created_at = models.DateTimeField(
        default=timezone.now
    )

    def is_low_stock(self):

        return self.quantity <= self.low_stock_alert
    
    def is_expired(self):

        return self.expiry_date < timezone.now().date()


    def expiring_soon(self):

        return (
            self.expiry_date -
            timezone.now().date()
        ).days <= 30 

    def __str__(self):

        return self.medicine_name

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

    medication_given = models.ForeignKey(
        MedicineStock,
        on_delete=models.CASCADE
    )

    quantity = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    
    dispensed_quantity = models.PositiveIntegerField(
        default=1
    )

    created_at = models.DateTimeField(
        default=timezone.now
    )

    def __str__(self):
        return f"Dispense - Visit {self.visit.id}"


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
    
# =====================================
# VITALS / TRIAGE
# =====================================

class Vital(models.Model):

    visit = models.OneToOneField(
        Visit,
        on_delete=models.CASCADE,
        related_name='vital'
    )

    blood_pressure = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    temperature = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        blank=True,
        null=True
    )

    pulse_rate = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    oxygen_saturation = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    respiratory_rate = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    weight = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        blank=True,
        null=True,
        help_text="Weight in KG"
    )

    height = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        blank=True,
        null=True,
        help_text="Height in CM"
    )

    bmi = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True
    )

    notes = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        default=timezone.now
    )

    def save(self, *args, **kwargs):

        if self.weight and self.height:

            height_in_meters = self.height / 100

            self.bmi = round(

                self.weight /

                (height_in_meters ** 2),

                2

            )

        super().save(*args, **kwargs)

    def bmi_status(self):

        if not self.bmi:

            return ""

        if self.bmi < 18.5:

            return "Underweight"

        elif self.bmi < 25:

            return "Normal"

        elif self.bmi < 30:

            return "Overweight"

        return "Obese"

    def __str__(self):

        return f"Vitals - Visit {self.visit.id}"
        
# =====================================
# APPOINTMENTS
# =====================================

class Appointment(models.Model):

    STATUS = (

        ('Pending', 'Pending'),

        ('Completed', 'Completed'),

        ('Missed', 'Missed'),

    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='appointments'
    )

    appointment_date = models.DateField()

    appointment_time = models.TimeField()

    reason = models.TextField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='Pending'
    )

    created_at = models.DateTimeField(
        default=timezone.now
    )

    def __str__(self):

        return f"{self.patient} - {self.appointment_date}" 
    
# =====================================
# PROCEDURES
# =====================================

PROCEDURE_TYPES = [

    ('Ultrasound', 'Ultrasound'),

    ('X-Ray', 'X-Ray'),

    ('ECG', 'ECG'),

    ('Physiotherapy', 'Physiotherapy'),

    ('Injection', 'Injection'),

    ('Dressing', 'Dressing'),

    ('Endoscopy', 'Endoscopy'),

    ('Minor Surgery', 'Minor Surgery'),

]
# =====================================
# TEST MODEL
# =====================================

class Test(models.Model):

    name = models.CharField(
        max_length=150,
        unique=True
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.name


# =====================================
# PROCEDURES
# =====================================

class Procedure(models.Model):

    visit = models.ForeignKey(
        Visit,
        on_delete=models.CASCADE,
        related_name='procedures'
    )

    procedure_name = models.CharField(
        max_length=100,
        choices=PROCEDURE_TYPES
    )

    notes = models.TextField(
        blank=True,
        null=True
    )

    image = models.ImageField(
        upload_to='procedure_images/',
        blank=True,
        null=True
    )

    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    performed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        default=timezone.now
    )

    def __str__(self):

        return self.procedure_name                   