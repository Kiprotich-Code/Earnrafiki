from django.db import models
from django.utils import timezone
from accounts.models import CustomUser

# Models 
class Account(models.Model):
    STATUS = [
        ('Active', 'active'),
        ('Inactive', 'inactive'),
        ('Pending', 'pending'),
        ('On Hold', 'on hold'),
        ('Closed', 'closed'),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='account')
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    status = models.CharField(max_length=50, choices=STATUS, default='pending')
    
    # Automatically pull the account number from CustomUser
    account_no = models.CharField(max_length=12, editable=False, unique=True)

    def deposit(self, amount):
        """Deposits money to the user's account"""
        self.balance += amount
        self.save()

    def withdraw(self, amount):
        """Withdraws money from the user's account, if sufficient balance exists"""
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
        self.save()

    def __str__(self):
        return f"Account of {self.user.email}, Account No: {self.account_no}, Balance: {self.balance}"


# Transaction model (to log deposits and withdrawals)
class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
    )

    STATUS = (
        ('Pending', 'pending'),
        ('Confirmed', 'confirmed'),
        ('Rejected', 'rejected'),
    )

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)
    tr_status = models.CharField(max_length=55, choices=STATUS, default='Pending')

    def save(self, *args, **kwargs):
        # Set default statuses based on transaction type
        if not self.id:  # Only when the transaction is first created
            if self.transaction_type == 'deposit':
                self.tr_status = 'Confirmed'  # Automatically approve deposits
            elif self.transaction_type == 'withdrawal':
                self.tr_status = 'Pending'  # Set withdrawals to pending by default

        # Prevent changes if the status is rejected
        if self.tr_status == 'Rejected' and self.pk is not None:
            raise ValueError("Cannot update a rejected transaction.")

        super(Transaction, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.transaction_type.capitalize()} of {self.amount} on {self.date}"