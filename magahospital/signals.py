from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from .models import Doctor_one, Receiption, Lab, Med_Prescription, Dispense_Medics
# Insertation of data to Doctor_one from Receiption
@receiver(post_save, sender=Receiption)
def create_doctor_from_receiption(sender, instance, created, **kwargs):
    if created:
        print(f"Signal triggered for Receiption: {instance.firstname} {instance.secondname}")
        
        def create_doctor():
            Doctor_one.objects.create(
                idno=instance,
                firstname=instance.firstname,
                secondname=instance.secondname,
                age=instance.age,
                address=instance.address,
                sex=instance.sex,
                date=instance.date
            )
        
        # Ensures Doctor_one is created *after* transaction is committed
        transaction.on_commit(create_doctor)

# Insertation of data from Doctor_one to Lab
@receiver(post_save, sender=Doctor_one)
def create_or_update_lab_from_doctor_one(sender, instance, created, **kwargs):
    if created:
        # Only if a new doctor is created
        Lab.objects.create(
            idno=instance,
            firstname=instance.firstname,
            secondname=instance.secondname,
            age=instance.age,
            address=instance.address,
            sex=instance.sex,
            date=instance.date,
            history=instance.history,
            lab_tests=instance.lab_tests
        )
    else:
        # If doctor is updated, also update the related lab (if it exists)
        try:
            lab = Lab.objects.get(idno=instance)
            lab.firstname = instance.firstname
            lab.secondname = instance.secondname
            lab.age = instance.age
            lab.address = instance.address
            lab.sex = instance.sex
            lab.date = instance.date
            lab.history = instance.history
            lab.lab_tests = instance.lab_tests
            lab.save()
        except Lab.DoesNotExist:
            # Optional: create if not found
            Lab.objects.create(
                idno=instance,
                firstname=instance.firstname,
                secondname=instance.secondname,
                age=instance.age,
                address=instance.address,
                sex=instance.sex,
                date=instance.date,
                history=instance.history,
                lab_tests=instance.lab_tests
            )
            
# insertation of data to med_prescription from Lab
@receiver(post_save, sender=Lab)
def create_or_update_med_prescription_from_lab(sender, instance, created, **kwargs):
    if created:
        # Only if a new doctor is created
        Med_Prescription.objects.create(
            idno=instance,
            firstname=instance.firstname,
            secondname=instance.secondname,
            age=instance.age,
            address=instance.address,
            sex=instance.sex,
            date=instance.date,
            history=instance.history,
            lab_tests=instance.lab_tests,
            lab_results = instance.lab_results
        )
    else:
        # If lab is updated, also update the related lab (if it exists)
        try:
            med_prescription = Med_Prescription.objects.get(idno=instance)
            med_prescription.firstname = instance.firstname
            med_prescription.secondname = instance.secondname
            med_prescription .age = instance.age
            med_prescription.address = instance.address
            med_prescription.sex = instance.sex
            med_prescription.date = instance.date
            med_prescription.history = instance.history
            med_prescription.lab_tests = instance.lab_tests
            med_prescription.lab_results = instance.lab_results
            med_prescription.save()
        except Lab.DoesNotExist:
            # Optional: create if not found
            Med_Prescription.objects.create(
                idno=instance,
                firstname=instance.firstname,
                secondname=instance.secondname,
                age=instance.age,
                address=instance.address,
                sex=instance.sex,
                date=instance.date,
                history=instance.history,
                lab_tests=instance.lab_tests,
                lab_results=instance.lab_results
            )
            
# insertation of data to dispense_medication from med_prescription
@receiver(post_save, sender=Med_Prescription)
def create_or_update_med_prescription_from_lab(sender, instance, created, **kwargs):
    if created:
        # Only if a new doctor is created
        Dispense_Medics.objects.create(
            idno=instance,
            firstname=instance.firstname,
            secondname=instance.secondname,
            age=instance.age,
            address=instance.address,
            sex=instance.sex,
            date=instance.date,
            history=instance.history,
            lab_tests=instance.lab_tests,
            lab_results = instance.lab_results,
            medical_prescription = instance.medical_prescription
        )
    else:
        # If  is updated, also update the related lab (if it exists)
        try:
            dispense_medics = Dispense_Medics.objects.get(idno=instance)
            dispense_medics.firstname = instance.firstname
            dispense_medics.secondname = instance.secondname
            dispense_medics.age = instance.age
            dispense_medics.address = instance.address
            dispense_medics.sex = instance.sex
            dispense_medics.date = instance.date
            dispense_medics.history = instance.history
            dispense_medics.lab_tests = instance.lab_tests
            dispense_medics.lab_results = instance.lab_results
            dispense_medics.medical_prescription = instance.medical_prescription
            dispense_medics.save()
        except Med_Prescription.DoesNotExist:
            # Optional: create if not found
            Med_Prescription.objects.create(
                idno=instance,
                firstname=instance.firstname,
                secondname=instance.secondname,
                age=instance.age,
                address=instance.address,
                sex=instance.sex,
                date=instance.date,
                history=instance.history,
                lab_tests=instance.lab_tests,
                lab_results=instance.lab_results,
                medical_prescription = instance.medical_prescription
            )