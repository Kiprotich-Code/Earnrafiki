from django.shortcuts import render, redirect
from .forms import PersonalInfoForm, AccountInfoForm, LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import datetime

# Create your views here.

# Step 1: Collect personal information
def signup_step1(request):
    if request.method == 'POST':
        form = PersonalInfoForm(request.POST)
        if form.is_valid():

            # Save personal info in session
            personal_info = form.cleaned_data
            request.session['personal_info'] = personal_info
            return redirect('signup_step2')
  
    else:
        form = PersonalInfoForm()

    return render(request, 'registration/signup_step1.html', {'form': form})

# Step 2: Collect email and password, and create the user
def signup_step2(request):
    personal_info = request.session.get('personal_info')
    if not personal_info:
        return redirect('signup_step1')  # Redirect to step 1 if personal info is missing

    if request.method == 'POST':
        form = AccountInfoForm(request.POST)
        if form.is_valid():
            # Create user with the data from both steps
            user = form.save(commit=False)
            # Set the personal info from step 1
            user.first_name = personal_info['first_name']
            user.last_name = personal_info['last_name']
            user.phone_no = personal_info['phone_no']
            user.address = personal_info['address']
            user.save()

            # Log in the user
            login(request, user)
            messages.success(request, 'Account Created Successfully!')
            return redirect('signin')  # Redirect to a dashboard or home page
    
    else:
        form = AccountInfoForm()
    
    return render(request, 'registration/signup_step2.html', {'form': form})


def signin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
                    
            # Redirect users based on role
            if user.is_staff:
                return redirect('dashboard')

            elif user.user_type in ['User', 'user']:
                return redirect('user_home')

            elif user.user_type.lower() == 'staff':
                return redirect('dashboard')
            
            else:
                messages.error('Could not determine your user type!')
                return redirect('signin')
        
        else:
            messages.error(request, 'User Does Not Exist!')
            return redirect('signin')

    else:
        form = LoginForm()
        
    context = {
            'form': form
        }
        
    return render(request, 'registration/signin.html', context)


def signout(request):
    logout(request)
    return redirect('home')