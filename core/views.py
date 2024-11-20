from django.shortcuts import render, redirect
from accounts.models import CustomUser
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm
from django.contrib.auth.decorators import login_required
from django.db import transaction

# Create your views here.
def home(request):
    return render(request, 'index.html')

def user_home(request):
    account = request.user.account
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


# ACCOUNTS VIEWS 
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


@login_required
def transaction_history_view(request):
    account = request.user.account
    transactions = account.transactions.all().order_by('-date')
    
    return render(request, 'accounts/transaction_history.html', {'transactions': transactions, 'account': account})


# USER VIEWS 
# my profile 
def my_profile(request):
    acc_no = request.user.account_no
    acc_info = Account.objects.get(user=request.user)
    user_info = CustomUser.objects.get(account_no=acc_no)
    return render(request, 'users/my_profile.html', {'acc_info': acc_info, 'user_info': user_info})