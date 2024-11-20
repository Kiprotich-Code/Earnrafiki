from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .managers import CustomUserManager

# Create your models here.
class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLES = [
        ('User', 'user'),
        ('Staff', 'staff'),
        ('Admin', 'admin'),
    ]   

    # personal details 
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    address = models.TextField(blank=True, null=True)
    phone_no = models.IntegerField(blank=True, null=True)

    # account details 
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    user_type = models.CharField(max_length=20, choices=ROLES, default='User')

    # account - field 
    account_no = models.CharField(max_length=12, unique=True, editable=False)


    # auth 
    password_reset_token = models.CharField(max_length=100, blank=True, null=True)
    password_reset_expiry = models.DateTimeField(blank=True, null=True)

    # manager 
    objects = CustomUserManager()

    # email as the default username 
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.email