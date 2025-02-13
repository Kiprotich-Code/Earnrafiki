from django.shortcuts import render, redirect
from .forms import UserForm, LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import datetime
from .models import CustomUser

# Create your views here.
def register(request):
    referral_code = request.GET.get('referral_code', None)
    referred_by = None
    
    # Check if a referral code exists and validate it
    if referral_code:
        try:
            referred_by = CustomUser.objects.get(referral_code=referral_code)
        except CustomUser.DoesNotExist:
            messages.error(request, 'Invalid referral code! Please make sure the code is correct and try again.')
            referred_by = None

    if request.method == 'POST':
        form = UserForm(request.POST)
                
        # Check if the form is valid
        if form.is_valid():
            # Passwords must match, so we check password and password2 fields
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']
            
            if password != password2:
                messages.error(request, 'Passwords do not match! Please ensure both passwords are the same.')
                return render(request, 'register.html', {'form': form, 'referral_code': referral_code})

            # Create the user and set the password properly
            user = form.save(commit=False)  # Don't save yet; we need to set the password
            user.set_password(password)  # Hash the password before saving
            user.save()  # Save the user

            # Optionally handle referred_by logic here if necessary

            messages.success(request, 'Registration successful!')
            return redirect('signin')  # Redirect to the signin page (or homepage)
        
        else:
            # If the form has errors, provide a more specific error message
            messages.error(request, 'There was an error with your form. Please ensure all fields are filled out correctly.')
            
    else:
        form = UserForm()

    # Pass the form and the referral code to the template
    return render(request, 'register.html', {'form': form, 'referral_code': referral_code})



def signin(request):
    if request.user.is_authenticated: 
        if request.user.is_staff:
            return redirect('dashboard')
            
        else:
            return redirect('user_home')
        
    else:
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
                
                else:
                    return redirect('user_home')
            
            else:
                try:
                    user = CustomUser.objects.get(email=email)
                    messages.error(request, 'Incorrect password! Please try again.')
                except CustomUser.DoesNotExist:
                    messages.error(request, 'User does not exist! Please check your email.')

                return redirect('signin')

        else:
            form = LoginForm()

        return render(request, 'registration/signin.html', {'form': form})


def signout(request):
    logout(request)
    return redirect('home')