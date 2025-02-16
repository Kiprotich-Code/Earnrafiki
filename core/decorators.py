from django.shortcuts import redirect
from django.urls import reverse

def activation_fee_required(view_func):
    """Redirect users to the activation fee payment page if they haven't paid."""
    def _wrapped_view(request, *args, **kwargs):
        # Check if the user is logged in and has a pending activation fee
        if request.user.is_authenticated and request.user.account.status.lower() == 'pending' and not request.user.account.activation_paid:
            # Redirect to the pay activation fee page if the activation fee isn't paid
            return redirect(reverse('user_home'))
        
        # If the user is eligible (either paid or status is active), call the view
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view
