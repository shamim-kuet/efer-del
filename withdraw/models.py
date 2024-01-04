from django.db import models
from django.contrib.auth import get_user_model
from wallet.models import Wallet

User = get_user_model()

withDraw_type = [
    ('CARD', 'Card'),
    ('BANK', 'Bank'),
]

class BankAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_bank_ac')
    # withdraw = models.ForeignKey(Withdraw, on_delete=models.CASCADE, null=True, blank=True)
    account_holder_name = models.CharField(max_length=50, null=True, blank=True)
    bank_name = models.CharField(max_length=50, null=True, blank=True)
    bank_area = models.CharField(max_length=50, null=True, blank=True)
    account_number = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    short_code = models.CharField(max_length=50, null=True, blank=True)
    expiry_date = models.DateField(blank=True, null=True)

    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)


class Withdraw(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_withdraw')
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='withdraw_wallet')
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, null=True, blank=True)
    withdraw_type = models.CharField(choices=withDraw_type, max_length=20, null=True, blank=True)
    withdraw_balance = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)

    is_confirmed = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)

    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']


    def __str__(self):
        return str(self.user)



