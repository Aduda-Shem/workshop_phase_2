# users/models.py
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _
from users.managers import UserManager

class User(AbstractUser):
    username = models.CharField(_('Username'), max_length=150, unique=True, blank=True, null=True)
    first_name = models.CharField(_('First Name'), max_length=100, blank=True, null=True)
    last_name = models.CharField(_('Last Name'), max_length=100, blank=True, null=True)
    email = models.EmailField(_('Email Address'), unique=True, null=False, db_index=True)
    phone_number = models.CharField(_('Phone Number'), max_length=100, blank=False, null=False)
    national_id = models.IntegerField(_('National Identification Number'), blank=True, null=True)
    image = models.ImageField(upload_to='media/profile_pics/', blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # Add related_name to resolve clashes
    groups = models.ManyToManyField(Group, verbose_name=_('groups'), blank=True, related_name='custom_user_set')
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='custom_user_set',
    )

    def __str__(self):
        return str(self.email)


class Company(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    supplies = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee')
    employee_id = models.CharField(_('Employee ID'), max_length=100, unique=True)
    department = models.CharField(_('Department'), max_length=100)
    first_name = models.CharField(_('First Name'), max_length=100)
    last_name = models.CharField(_('Last Name'), max_length=100)
    national_id = models.CharField(_('National ID'), max_length=100, unique=True)
    phone_number = models.CharField(_('Phone Number'), max_length=100)
    salary = models.DecimalField(_('Salary'), max_digits=10, decimal_places=2)

    def __str__(self):
        return self.user.email