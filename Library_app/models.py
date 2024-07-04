from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date, datetime, timedelta
from django.conf import settings

class User(AbstractUser):
    is_staff = models.BooleanField(default=False)
    is_student=models.BooleanField(default=False)

class Book(models.Model):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)  # Changed to CharField for 13-digit ISBN
    category = models.CharField(max_length=50)
    publication = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} [{self.isbn}]"

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    dept = models.CharField(max_length=10)
    branch = models.CharField(max_length=100)
    register_no = models.CharField(max_length=10, unique=True)
    phone = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.user} [{self.dept}] [{self.register_no}]"

def expiry():
    return datetime.today() + timedelta(days=14)

def expiry1():
    return datetime.today() + timedelta(days=29)

class StudentIssuedBookManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        for book in qs:
            book.update_fine()
        return qs
    
class studentIssuedBook(models.Model):
    student_register_no = models.CharField(max_length=100)
    book = models.CharField(max_length=100)
    isbn = models.CharField(max_length=10)
    issued_date = models.DateField(auto_now=True)
    expiry_date = models.DateField(default=expiry)
    fine = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    objects = StudentIssuedBookManager()

    def calculate_fine(self):
        today = date.today()
        expiry_date = self.expiry_date
        if isinstance(expiry_date, datetime):
            expiry_date = expiry_date.date()

        if expiry_date < today:
            overdue_days = (today - expiry_date).days
            if overdue_days > 45:
                return overdue_days * 5.00
            else:
                return overdue_days * 1.00
        return 0.00

    def update_fine(self):
        self.fine = self.calculate_fine()
        self.save()

    def save(self, *args, **kwargs):
        self.fine = self.calculate_fine()
        super().save(*args, **kwargs)

class Staff(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    dept = models.CharField(max_length=10)
    branch = models.CharField(max_length=100)
    staff_id = models.CharField(max_length=10, unique=True)
    phone = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.user} [{self.branch}] [{self.staff_id}]"


class StaffIssuedBookManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        for book in qs:
            book.update_fine()
        return qs

class staffIssuedBook(models.Model):
    staff_id = models.CharField(max_length=100)
    book = models.CharField(max_length=100) 
    isbn=models.CharField(max_length=10)
    issued_date = models.DateField(auto_now=True)
    expiry_date = models.DateField(default=expiry1)
    fine = models.DecimalField(max_digits=6, decimal_places=2, default=0.00) 
    objects = StaffIssuedBookManager()
    def calculate_fine(self):
        today = date.today() 
        if self.expiry_date < today:
            overdue_days = (today - self.expiry_date).days
            if(overdue_days>45):
                return overdue_days * 5.00
            else:
                return overdue_days*1.00 
        return 0.00

    def update_fine(self):
        self.fine = self.calculate_fine()
        self.save()

    def save(self, *args, **kwargs):
        self.fine = self.calculate_fine()
        super().save(*args, **kwargs)
    
