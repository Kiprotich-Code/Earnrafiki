# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

# Step 1: Personal Information Form
class UserForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@gmail.com'}))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password',
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Confirm Password',
            }
        )
    )

    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'phone_no', 'password', ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Name"}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Email"}),
            'phone_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Phone Number"}),
        }


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder' :'Email', 'style': 'max-width: 600px;'}))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter Password',
                'style': 'max-width: 600px;'
            }
        )
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Confirm Password',
                'style': 'max-width: 600px;'
            }
        )
    )