from django.db import models
from django.core.exceptions import ValidationError

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
class Doctor(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='doctors/', blank=True, null=True)
    qualification = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    def is_available(self, start_time):
    # Check if the doctor is available during the given start time
        overlapping_appointments = Appointment.objects.filter(
            doctor=self,
            start_time__lt=start_time
        )
        return not overlapping_appointments.exists()
class TimeSlot(models.Model):
    start_time = models.TimeField()
    # end_time = models.TimeField()

    def __str__(self):
        return f"{self.start_time}"

    def is_overlapping(self, new_start_time):
        return (
            self.start_time < new_start_time
        )

    def clean(self):
        appointments = Appointment.objects.filter(time_slot=self)
        for appointment in appointments:
            if self.is_overlapping(appointment.start_time):
                raise ValidationError('Overlapping appointments are not allowed.')

class Appointment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    place = models.CharField(max_length=100)
    date = models.DateField()
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    status_choices = [('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')]
    status = models.CharField(max_length=10, choices=status_choices, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.date} {self.time_slot}"
# class Admin(models.Model):
#     name = models.CharField(max_length=100)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=100)
#     def __str__(self) :
#         return self.name
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('superadmin', 'Super Admin'),
        ('admin', 'Admin'),
        ('user', 'User'),
    )
    email = models.EmailField(default='example@example.com')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)


