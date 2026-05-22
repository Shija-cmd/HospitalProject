from django.test import TestCase
from django.contrib.auth.models import User

from .models import Patient, Visit


class WorkflowTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username='doctor',
            password='1234'
        )

        self.patient = Patient.objects.create(
            firstname='John',
            secondname='Doe',
            age=25,
            address='Test Address',
            sex='M'
        )

    # =====================================
    # TEST VISIT CREATION
    # =====================================

    def test_visit_creation(self):

        visit = Visit.objects.create(
            patient=self.patient
        )

        self.assertEqual(
            visit.status,
            'Waiting Vital'
        )
        
    # =====================================
    # TEST VITALS FLOW
    # =====================================

    def test_vitals_flow(self):

        visit = Visit.objects.create(
            patient=self.patient
        )

        # simulate vitals completion
        visit.status = 'Waiting Doctor'

        visit.save()

        self.assertEqual(
            visit.status,
            'Waiting Doctor'
        )
        
    # =====================================
    # TEST PROCEDURE FLOW
    # =====================================

    def test_procedure_flow(self):

        visit = Visit.objects.create(
            patient=self.patient
        )

        # simulate procedure completion
        visit.status = 'Doctor Review'

        visit.save()

        self.assertEqual(
            visit.status,
            'Doctor Review'
        )
        
    # =====================================
    # TEST BILLING FLOW
    # =====================================

    def test_billing_flow(self):

        visit = Visit.objects.create(
            patient=self.patient
        )

        # simulate cashier completion
        visit.status = 'Dispense'

        visit.save()

        self.assertEqual(
            visit.status,
            'Dispense'
        )
        
    # =====================================
    # TEST DOCTOR REVIEW QUEUE
    # =====================================

    def test_doctor_review_queue(self):

        visit = Visit.objects.create(
            patient=self.patient,
            status='Doctor Review'
        )

        doctor_queue = Visit.objects.filter(
            status='Doctor Review'
        )

        self.assertIn(
            visit,
            doctor_queue
        )           