from django.contrib import admin
from .models import Withdraw, BankAccount

# Register your models here.
class WithdrawAdmin(admin.ModelAdmin):
    list_display = ['user', 'withdraw_balance', 'is_confirmed', 'is_paid', 'active']
    search_fields = ['user']
    list_filter = ['user']

    class Meta:
        model = Withdraw

admin.site.register(Withdraw, WithdrawAdmin)

class BankAccountAdmin(admin.ModelAdmin):
    list_display = ['user', 'account_holder_name', 'bank_name', 'account_number','country', 'active']
    search_fields = ['user', 'account_holder_name']
    list_filter = ['user', 'account_holder_name']

    class Meta:
        model = BankAccount


admin.site.register(BankAccount, BankAccountAdmin)
