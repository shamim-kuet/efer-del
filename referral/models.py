from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from efranchise.utils import unique_referral_code_generator
# from wallet.models import Wallet
from django.utils import timezone

User = get_user_model()


class Referral(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referrer_user')
    referral_code = models.CharField(max_length=30)
    referral_discount = models.DecimalField(max_digits=7, decimal_places=2, default=10.00)
    is_percent = models.BooleanField(default=True)
    total_referral = models.IntegerField(default=0)
    total_referral_income = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    purchase_limit_per_user = models.IntegerField(default=3)
    minimum_purchase_per_user = models.DecimalField(max_digits=7, decimal_places=2, default=10.00)
    number_of_referral_confirmed_purchase = models.IntegerField(default=0)

    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def referrer_discount(self):
        if self.number_of_referral_confirmed_purchase > 0:
            ans = self.number_of_referral_confirmed_purchase / 3
            mod = self.number_of_referral_confirmed_purchase % 3
            total_referral_income = float(ans) * float(self.referral_discount)
            return total_referral_income
        # sum_price = 0
        # total_referred = self.referral_user.all()
        # for i in total_referred:
        #     sum_price += i.total_purchase_amount
        # print(sum_price)
        # discount_percent = (sum_price * self.referral_discount) / 100
        # print(discount_percent)
        # return discount_percent

    def __str__(self):
        return self.referral_code

    class Meta:
        verbose_name = '  Referral'
        verbose_name_plural = '  Referrals'

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        ref_code = unique_referral_code_generator(Referral, name=instance.first_name)
        if created:
            Referral.objects.create(user=instance, referral_code=ref_code)


class ReferredPerson(models.Model):
    referral = models.ForeignKey(Referral, on_delete=models.CASCADE, related_name='referral_user', null=True,
                                 blank=True)
    referred_person_name = models.CharField(max_length=50, null=True, blank=True)
    referred_person_country = models.CharField(max_length=50, null=True, blank=True)
    referred_person_id = models.CharField(max_length=50)
    referred_person_email = models.EmailField(max_length=50, null=True, blank=True)
    referred_person_last_order_amount = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    total_purchase_time = models.IntegerField(default=0)
    total_purchase_amount = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)

    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def purchase_diff(self):
        if self.total_purchase_time <= 1:
            now = timezone.localtime(timezone.now())
            dif = now - self.updated_at
            return dif.days
        return None

    def __str__(self):
        return f'{self.referral}'

    class Meta:
        verbose_name = ' Referred Person'
        verbose_name_plural = ' Referred Person'


class ReferralReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_referral_report')
    Date = models.DateField(null=True, blank=False)
    profit = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    company_profit = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)

    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'Referral Report'
        verbose_name_plural = 'Referral Report'

    @property
    def month(self):
        if self.Date:
            return self.Date.strftime("%B")
        return "No date entry"

    @property
    def year(self):
        if self.Date:
            return self.Date.strftime("%Y")
        return "No date entry"

    @property
    def total_profit(self):
        return self.profit + self.company_profit
