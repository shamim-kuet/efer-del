from django.contrib import admin
from .models import Wallet

# Register your models here.
class WalletAdmin(admin.ModelAdmin):
    list_display = ['user', 'balance', 'minimum_withdraw', 'company_profit', 'active']
    search_fields = ['user']
    list_filter = ['user']

    class Meta:
        model = Wallet

admin.site.register(Wallet, WalletAdmin)
