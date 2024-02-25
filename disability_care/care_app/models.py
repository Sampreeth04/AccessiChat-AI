from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings


# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, user_id, first_name, last_name, email, role, address_line_1, city, state, country, zip_code, password=None, **extra_fields):
        if not user_id:
            raise ValueError('The User ID field must be set')
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(user_id=user_id, first_name=first_name, last_name=last_name, email=email, role=role, address_line_1=address_line_1, city=city, state=state, country=country, zip_code=zip_code, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, first_name, last_name, email, role, address_line_1, city, state, country, zip_code, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(user_id, first_name, last_name, email, role, address_line_1, city, state, country, zip_code, password, **extra_fields)

class User(AbstractBaseUser):
    ROLES = [
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('caretaker', 'Caretaker'),
    ]

    user_id = models.CharField(primary_key=True, max_length=10, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=5)
    role = models.CharField(max_length=20, choices=ROLES)
    password = models.CharField(max_length=128)

    # Required fields for custom user model
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_id', 'first_name', 'last_name', 'address_line_1', 'city', 'state', 'country', 'zip_code', 'role']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"

class PatientInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=255)
    hospital = models.CharField(max_length=255)
    pharmacy = models.CharField(max_length=255)
    diagnosis = models.TextField()
    medication = models.TextField()
    doctor = models.ForeignKey(User, related_name='patients_doctor', on_delete=models.CASCADE)
    caretaker = models.ForeignKey(User, related_name='patients_caretaker', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Medication(models.Model):
    medicine_id = models.CharField(max_length=10, unique=True, primary_key=True)
    medicine_name = models.CharField(max_length = 50)

    patient_id = models.ForeignKey(User, on_delete=models.CASCADE)

    #date = models.DateField()
    day_choices = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ]

    day = models.CharField(max_length=20, choices=day_choices)

    time_choices = [
        ('morning', 'Morning'),
        ('afternoon', 'Afternoon'),
        ('evening', 'Evening')
    ]
    time = models.CharField(max_length=20, choices=time_choices)
    amount = models.CharField(max_length=100)
    dosage = models.CharField(max_length = 15)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Medication ID: {self.medicine_id}"
    
class Appointment(models.Model):
    appointment_id = models.CharField(max_length=10, unique=True)
    patient_id = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    # time_choices = models.CharField(max_length=20)  # Store time as a string

    # time = models.CharField(max_length=20, choices=time_choices)
    time = models.CharField(max_length=20)  # Store time as a string

    appointment_details = models.TextField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Appointment ID: {self.appointment_id}"

