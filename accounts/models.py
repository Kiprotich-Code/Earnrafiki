from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .managers import CustomUserManager
import uuid

# Create your models here.
class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLES = [
        ('User', 'user'),
        ('Staff', 'staff'),
        ('Admin', 'admin'),
    ]   

    # personal details 
    name = models.CharField(max_length=30, blank=False)
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

    # refferal code 
    referral_code = models.CharField(max_length=12, unique=True, blank=True, null=True)

    # auth 
    password_reset_token = models.CharField(max_length=100, blank=True, null=True)
    password_reset_expiry = models.DateTimeField(blank=True, null=True)

    # manager 
    objects = CustomUserManager()

    # email as the default username 
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = str(uuid.uuid4()).split('-')[0]  # Generate a short unique code
        super(CustomUser, self).save(*args, **kwargs)

    def __str__(self):
        return self.email