from django.db import models
from django.contrib.auth.models import User
from departments.models import Department


class Employee(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="employee_profile"
    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)

    designation = models.CharField(max_length=100)
    ROLE_CHOICES = [
    ("Employee", "Employee"),
    ("Manager", "Manager"),
    ("HR", "HR"),
]

    role = models.CharField(
    max_length=20,
    choices=ROLE_CHOICES,
    default="Employee"
)

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="employees",
        null=True,
        blank=True,
    )

    date_of_joining = models.DateField()
    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.first_name} {self.last_name}"