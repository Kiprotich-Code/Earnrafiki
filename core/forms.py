from django import forms
from .models import Transaction


class DepositForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount']

class WithdrawForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount']

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 100:
            raise forms.ValidationError("Amount must be more than 100.")
        return amount