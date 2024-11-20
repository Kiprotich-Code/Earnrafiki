from django.shortcuts import render, redirect, get_object_or_404
from .forms import AddUserForm, UpdateUserForm
from accounts.models import CustomUser
from django.views.generic import ListView , DeleteView, DetailView, UpdateView
from core.models import Account, Transaction
from django.utils import timezone
from django.db.models import Sum, Q

# Create your views here.
def dashboard(request):
    accounts = Account.objects.all()[0:10]
    accounts_count = Account.objects.all().count()
    # New accounts created today
    today = timezone.now().date()
    new_accounts = CustomUser.objects.filter(date_joined__date=today).count() 
    # Total cash in all accounts (assuming 'balance' is the field in the Account model)
    total_cash = Account.objects.aggregate(total_balance=Sum('balance'))['total_balance'] or 0

    transactions_today = Transaction.objects.filter(date__date=today)
    total_balance_today = transactions_today.aggregate(
        total_deposits=Sum('amount', filter=Q(transaction_type='deposit')),
        total_withdrawals=Sum('amount', filter=Q(transaction_type='withdrawal'))
    )
    total_balance_today = (total_balance_today['total_deposits'] or 0) - (total_balance_today['total_withdrawals'] or 0)

    # all transactions 
    transactions = Transaction.objects.all().order_by('-date')[0:3]
    transactions_count = Transaction.objects.all().count()

    context = {
        'accounts': accounts,
        'accounts_count': accounts_count, 
        'new_accounts': new_accounts,
        'total_cash':total_cash,
        'total_balance_today': total_balance_today,
        'transactions': transactions,
        'transactions_count': transactions_count
    }
    return render(request, 'dashboard.html', context)

# CRUD ON USERS 
# CREATE - USER 
def add_user(request):
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ctrl_users')
        
    else: 
        form = AddUserForm()

    return render(request, 'users/add_user.html', {'form': form})

# List View 
def ctrl_users(request):
    users = CustomUser.objects.all()
    return render(request, 'users/ctrl_users.html', {'users': users})

# Detail View 
def update_user(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('ctrl_users')
        
    else:
        form = UpdateUserForm(instance=user)
    return render(request, 'users/update_user.html', {'form': form})


def user_details(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    return render(request, 'users/user_details.html', {'user': user})


# CRUD ON ACCOUNTS
class AccountListView(ListView):
    context_object_name = 'accounts'
    model = Account
    template_name = 'accounts/accounts.html'
    paginate_by = 5

def update_account(request, id):
    acc = Account.objects.get(id=id)  # Fetch the account object or return 404 if not found
    user = CustomUser.objects.get(account_no = acc.account_no)
    if request.method == 'POST':
        new_status = request.POST.get('status')  # Get the status from the button value
        if new_status:
            acc.status = new_status  # Update the account's status
            acc.save()  # Save the change to the database
            return redirect('accounts')  # Redirect to account detail page or another appropriate page
    
    return render(request, 'accounts/account_update.html', {'acc': acc, 'user': user})


class AccountDeleteView(DeleteView):
    model = Account
    success_url = '/dashboad/accounts/'
    template_name = 'accounts/confirm_delete_account.html'


# TRANSACTION VIEWS
class TransactionListView(ListView):
    context_object_name = 'transactions'
    model = Transaction
    template_name = 'transactions/transactions.html'
    paginate_by = 10


def update_transaction(request, id):
    transaction = get_object_or_404(Transaction, id=id)

    # Prevent updates to rejected transactions
    if transaction.tr_status == 'Rejected':
        return render(request, 'transactions/transaction_update.html', {
            'transaction': transaction,
            'error_message': 'Rejected transactions cannot be modified.'
        })

    if request.method == 'POST':
        new_status = request.POST.get('tr_status')  # Get the status from the button value
        if new_status:
            transaction.tr_status = new_status
            transaction.save()  # Save the change to the database
            return redirect('transactions')  # Redirect to transaction list page or another appropriate page
    
    return render(request, 'transactions/transaction_update.html', {'transaction': transaction})


# ADMIN PROFILE 
def admin_profile(request):
    admin_info = CustomUser.objects.get(id=request.user.id)
    return render(request, 'admin_profile.html', {'admin_info': admin_info})