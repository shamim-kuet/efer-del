from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import ReferralReport, ReferredPerson, Referral


class ReferredPersonSerializer(ModelSerializer):

    class Meta:
        model = ReferredPerson
        fields = ['id', 'referred_person_name', 'referred_person_id', 'total_purchase_time', 'updated_at', "purchase_diff",
                  'referred_person_email', 'total_purchase_amount', 'referred_person_country' ]


class ReferralSerializer(ModelSerializer):
    # referral = ReferredPersonSerializer(source='referral_user', many=True, read_only=True)
    referral = SerializerMethodField(read_only=True)

    class Meta:
        model = Referral
        fields = ['id', 'referral_code', 'referral', 'total_referral_income']

    def get_referral(self, instance):
        qs = instance.referral_user.all().order_by('-pk')
        return ReferredPersonSerializer(qs, many=True).data


class ReferralReportSerializer(ModelSerializer):

    class Meta:
        model = ReferralReport
        fields = ['user', 'Date', 'profit', 'company_profit', 'month', 'year', 'total_profit']