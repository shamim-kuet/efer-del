from rest_framework import serializers
from .models import User, UserDetails, EFranchiseInfo, EHubInfo, EHubPurchasePerson
from django.utils.translation import gettext_lazy as _
import re


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name',
                  'last_name', 'phone_number', 'role', 'is_confirmed', 'is_blocked', 'is_active']


class EFranchiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = EFranchiseInfo
        fields = ['id', 'three_years_store_number', 'five_years_store_number', 'total_liquid_assets', 'total_net_worth',
                  'start_date', 'end_date', 'bank_statement', 'status']


class EHubSerializer(serializers.ModelSerializer):
    class Meta:
        model = EHubInfo
        fields = ['id', 'space_type', 'space_description', 'space_img', 'space_video',
                  'available_from', 'is_delivery_man', 'delivery_vehicles', 'start_date', 'end_date', 'contact_year',
                  'status']


class EHubShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = EHubInfo
        fields = ['id', 'space_type', 'space_img',
                  'available_from', 'is_delivery_man', 'delivery_vehicles', 'start_date', 'end_date',
                  'status']


class UserWithProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    e_franchise_hub = serializers.SerializerMethodField()

    class Meta:
        model = UserDetails
        fields = '__all__'
        read_only_fields = ['id', 'user', 'created_at', 'updated_at', 'e_franchise_hub']

    def get_e_franchise_hub(self, obj):
        request = self.context.get("request")
        if obj.user.role == 'FRANCHISE':
            qs = EFranchiseInfo.objects.filter(user_id=obj.user.id).first()
            serializer = EFranchiseSerializer(qs, context={'request': request})
            return serializer.data
        elif obj.user.role == 'HUB':
            qs = EHubInfo.objects.filter(user_id=obj.user.id).first()
            serializer = EHubSerializer(qs, context={'request': request})
            return serializer.data
        return None


class ResetPasswordSerializer(serializers.Serializer):
    identifier = serializers.CharField()


class ResetPasswordConfirmSerializer(serializers.Serializer):
    password = serializers.CharField()

    def validate_password(self, password):
        if len(password) < 8:
            raise serializers.ValidationError(
                _("This password is too short. It must contain at least 8 character."),
                code='password_too_short',
            )
        # if not re.findall('\d', password):
        #     raise serializers.ValidationError(
        #         _("The password must contain at least 1 digit, 0-9."),
        #         code='password_no_number',
        #     )
        # if not re.findall('[A-Z]', password):
        #     raise serializers.ValidationError(
        #         _("The password must contain at least 1 uppercase letter, A-Z."),
        #         code='password_no_upper',
        #     )
        # if not re.findall('[a-z]', password):
        #     raise serializers.ValidationError(
        #         _("The password must contain at least 1 lowercase letter, a-z."),
        #         code='password_no_lower',
        #     )

        return password


class EHubPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = EHubPurchasePerson
        fields = ['id', 'hub', 'person_name', 'person_id', 'person_email', 'number_of_sells_product',
                  'total_amount_of_sells_product', 'invoice', 'active', 'Date']


class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'email']


class EHubDetailsSerializer(serializers.ModelSerializer):
    user = UserShortSerializer(read_only=True)

    class Meta:
        model = EHubInfo
        fields = ['id', 'space_type', 'space_description', 'space_img', 'space_video',
                  'available_from', 'is_delivery_man', 'delivery_vehicles', 'start_date', 'end_date', 'contact_year',
                  'status', 'user']
