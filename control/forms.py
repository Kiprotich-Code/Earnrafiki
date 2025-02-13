from accounts.models import CustomUser
from django import forms
from django.contrib.auth.forms import UserChangeForm
from core.models import Account

# Forms 
class AddUserForm(forms.ModelForm):
    class Meta:
        model  = CustomUser
        fields = ['name', 'phone_no', 'email', 'password', ]
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control',  'style': 'max-width: 600px', 'placeholder': "Email Address"}),
            'name': forms.TextInput(attrs={'class': 'form-control',  'style': 'max-width: 600px', 'placeholder': "Name"}),
            'phone_no': forms.TextInput(attrs={'class': 'form-control',  'style': 'max-width: 600px', 'placeholder': "Phone No"}),
            'password': forms.PasswordInput(attrs={'class': 'form-control',  'style': 'max-width: 600px', 'placeholder': "Enter Password"}),
        }



class UpdateUserForm(UserChangeForm):
    password = None
    class Meta:
        model = CustomUser
        fields = ['name', 'phone_no', 'email', ]
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control',  'style': 'max-width: 600px', 'placeholder': "Email Address"}),
            'name': forms.TextInput(attrs={'class': 'form-control',  'style': 'max-width: 600px', 'placeholder': "First Name"}),
            'phone_no': forms.TextInput(attrs={'class': 'form-control',  'style': 'max-width: 600px', 'placeholder': "Phone No"}),
        }


class UpdateAccountStatusForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['status']