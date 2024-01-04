from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Wallet


class WalletSerializer(ModelSerializer):
    # monthly_profit = SerializerMethodField(read_only=True)

    # balance = SerializerMethodField(read_only=True)

    class Meta:
        model = Wallet
        fields = ['id', 'user', 'balance', 'total_profit', 'active']

