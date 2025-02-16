from django.shortcuts import render, redirect
from accounts.models import CustomUser
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from .decorators import activation_fee_required

# Create your views here.
def home(request):
    return render(request, 'index.html')

def user_home(request):
    account = request.user.account
    
    if account.status in ['Pending', 'pending'] and not account.activation_paid:
        return render(request, 'accounts/pending.html', {'account': account})

    transactions = Transaction.objects.filter(account=account).order_by('-date')[0:10]
    transaction_count = transactions.count()
    pending_transaction_count = Transaction.objects.filter(account=account, tr_status='Pending').count()
    confirmed_transaction_count = Transaction.objects.filter(account=account, tr_status='Confirmed').count()

    context = {
        'transactions': transactions,
        'transaction_count': transaction_count,
        'pending_transaction_count': pending_transaction_count,
        'confirmed_transaction_count': confirmed_transaction_count
    }
    return render(request, 'user_home.html', context)




def pay_activation_fee(request):
    account = request.user.account
    
    if account.activation_paid:
        messages.success(request, "Your account is already activated!")
        return redirect('user_home')
    
    if account.balance >= 500:  # Ensure the user has enough funds to pay the activation fee
        account.balance -= 500  # Deduct the activation fee from the balance
        account.activation_paid = True  # Mark the activation as paid
        account.set_status_based_on_payment()  # Update the account status
        account.save()
        messages.success(request, "Activation fee paid successfully! Your account is now active.")
    else:
        messages.error(request, "Insufficient funds to pay the activation fee. Please deposit money to proceed.")
        return render(request, 'deposit_prompt.html')  # Render a page with a "Deposit Money" CTA
    
    return redirect('user_home')


# ACCOUNTS VIEWS 
@activation_fee_required
@login_required
def acc_details(request):
    acc = Account.objects.get(user=request.user)

    context = {
        'acc': acc
    }

    return render(request, 'accounts/acc_details.html', context)

# TRANSACT 
# deposit 
@login_required
def deposit_view(request):
    account = request.user.account
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                # Create a transaction record
                transaction_record = form.save(commit=False)
                transaction_record.account = account
                transaction_record.transaction_type = 'deposit'
                transaction_record.save()

                # Update the account balance
                account.balance += transaction_record.amount
                account.save()

            return redirect('transaction_history')
    else:
        form = DepositForm()

    return render(request, 'accounts/deposit.html', {'form': form, 'account': account})

@activation_fee_required
@login_required
def withdraw_view(request):
    account = request.user.account
    if request.method == 'POST':
        form = WithdrawForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                # Check if the account has enough balance
                amount = form.cleaned_data['amount']
                if account.balance >= amount:
                    # Create a transaction record
                    transaction_record = form.save(commit=False)
                    transaction_record.account = account
                    transaction_record.transaction_type = 'withdrawal'
                    transaction_record.save()

                    # Update the account balance
                    account.balance -= amount
                    account.save()
                else:
                    form.add_error('amount', 'Insufficient funds')

            return redirect('transaction_history')
    else:
        form = WithdrawForm()

    return render(request, 'accounts/withdraw.html', {'form': form, 'account': account})


@activation_fee_required
@login_required
def transaction_history_view(request):
    account = request.user.account
    transactions = account.transactions.all().order_by('-date')
    
    return render(request, 'accounts/transaction_history.html', {'transactions': transactions, 'account': account})


# USER VIEWS 
# my profile
@activation_fee_required
@login_required 
def my_profile(request):
    acc_no = request.user.account_no
    acc_info = Account.objects.get(user=request.user)
    user_info = CustomUser.objects.get(account_no=acc_no)
    return render(request, 'users/my_profile.html', {'acc_info': acc_info, 'user_info': user_info})