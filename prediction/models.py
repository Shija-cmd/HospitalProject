from django.db import models
from django.contrib.auth.models import User
import random
import joblib

# RANDOM PATIENT CODE
def generate_random_code():
    return str(random.randint(100000000, 999999999))

# GENDER CHOICES
SEX = (
    ('Male', 'Male'),
    ('Female', 'Female'),
)

# HOSPITAL CHOICES
hosp = (
    ('Magadulla Hospital', 'Magadulla Hospital'),
)

# SYMPTOM CHOICES
YES_NO = (
    (1, 'Yes'),
    (0, 'No'),
)


class Patient(models.Model):

    jina_la_mtumiaji = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    tarehe = models.DateField(
        null=True,
        blank=True,
        auto_now_add=True
    )

    jina_la_kwanza = models.CharField(
        max_length=200,
        verbose_name="First Name"
    )

    jina_la_pili = models.CharField(
        max_length=200,
        verbose_name="Last Name"
    )

    simu = models.CharField(
        max_length=200,
        verbose_name="Phone Number"
    )

    anwani = models.TextField(
        null=True,
        blank=True,
        verbose_name="Address"
    )

    jinsia = models.CharField(
        max_length=20,
        choices=SEX,
        verbose_name="Gender"
    )

    umri = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Age"
    )

    Namba_ya_mgonjwa = models.CharField(
        max_length=9,
        default=generate_random_code,
        db_index=True,
        editable=False
    )

    DALILI1 = models.PositiveIntegerField(
        choices=YES_NO,
        verbose_name="Genital sores"
    )

    DALILI2 = models.PositiveIntegerField(
        choices=YES_NO,
        verbose_name="Pain during urination"
    )

    DALILI3 = models.PositiveIntegerField(
        choices=YES_NO,
        verbose_name="Unusual discharge"
    )

    DALILI4 = models.PositiveIntegerField(
        choices=YES_NO,
        verbose_name="Lower abdominal pain"
    )

    DALILI5 = models.PositiveIntegerField(
        choices=YES_NO,
        verbose_name="Skin rash"
    )

    hospitali = models.CharField(
        max_length=100,
        choices=hosp,
        default='Magadulla Hospital',
        verbose_name="Hospital"
    )

    MAAMBUKIZI = models.CharField(
        max_length=100,
        blank=True,
        editable=False,
        verbose_name="Prediction"
    )

    # NEW CONFIDENCE FIELD
    CONFIDENCE = models.FloatField(
        null=True,
        blank=True,
        editable=False,
        verbose_name="Confidence (%)"
    )

    created = models.DateTimeField(auto_now_add=True)

    # MACHINE LEARNING PREDICTION
    def save(self, *args, **kwargs):

        ml_model = joblib.load('prediction/ml_model/model.joblib')

        # PREDICTION
        prediction = ml_model.predict([[
            self.DALILI1,
            self.DALILI2,
            self.DALILI3,
            self.DALILI4,
            self.DALILI5
        ]])

        # PROBABILITY / CONFIDENCE
        probabilities = ml_model.predict_proba([[
            self.DALILI1,
            self.DALILI2,
            self.DALILI3,
            self.DALILI4,
            self.DALILI5
        ]])

        confidence = max(probabilities[0]) * 100

        self.CONFIDENCE = round(confidence, 2)

        # CLEAN RESULT
        result = str(prediction[0]).strip().lower()

        # FINAL DISPLAY RESULT
        if result == "kuna maambukizi":

            self.MAAMBUKIZI = "Potential Infection Detected"

        else:

            self.MAAMBUKIZI = "Low Infection Risk Detected"

        return super().save(*args, **kwargs)

    def __str__(self):
        return self.jina_la_kwanza

    class Meta:
        ordering = ['jina_la_mtumiaji']