from django.contrib import admin
from .models import Referral, ReferredPerson, ReferralReport

# Register your models here.
class ReferralAdmin(admin.ModelAdmin):
    list_display = ['user', 'referral_code', 'referral_discount', 'referral_discount', 'total_referral_income',
                    'number_of_referral_confirmed_purchase', 'active']
    search_fields = ['user']
    list_filter = ['user']

    class Meta:
        model = Referral

admin.site.register(Referral, ReferralAdmin)

class ReferredPersonAdmin(admin.ModelAdmin):
    list_display = ['referral', 'referred_person_name', 'referred_person_email', 'total_purchase_amount', 'active']
    search_fields = ['referral', 'referred_person_name']
    list_filter = ['referral', 'referred_person_name']

    class Meta:
        model = ReferredPerson


admin.site.register(ReferredPerson, ReferredPersonAdmin)

class ReferralReportAdmin(admin.ModelAdmin):
    list_filter = ['Date', 'user']

    class Meta:
        model = ReferralReport
admin.site.register(ReferralReport, ReferralReportAdmin)
