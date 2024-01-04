from rest_framework.serializers import ModelSerializer
from .models import Withdraw, BankAccount


class BankAccountSerializer(ModelSerializer):

    class Meta:
        model = BankAccount
        fields = ['id', 'account_holder_name', 'bank_name','bank_area', 'country', 'account_number',
                  'expiry_date', 'short_code']
        read_only_fields = ['user']


class BankAccountForWithdrawHistorySerializer(ModelSerializer):

    class Meta:
        model = BankAccount
        fields = ['id', 'bank_name', 'country', 'account_number']
        read_only_fields = ['user']


class WithdrawSerializer(ModelSerializer):
    bank_account = BankAccountForWithdrawHistorySerializer(read_only=True)

    class Meta:
        model = Withdraw
        fields = ['id', 'user', 'wallet', 'bank_account_id', 'bank_account', 'withdraw_type', 'withdraw_balance',
                  'is_confirmed', 'is_paid', 'created_at']
        read_only_fields = ['user', 'wallet', 'created_at']
        extra_kwargs = {
            'bank_account_id': {'source': 'bank_account', 'write_only': True},
        }
