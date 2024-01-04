from django.db import models
from django.db.models.signals import post_save, pre_save
from django.contrib.auth import get_user_model
from referral.models import Referral, ReferralReport
from django.utils.timezone import localtime, now
from django.db.models.functions import TruncMonth, TruncYear

User = get_user_model()


class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_wallet')
    balance = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    reword_point = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    minimum_withdraw = models.DecimalField(max_digits=7, decimal_places=2, default=6.00)
    # referral_profit = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    company_profit = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    # total_withdraw = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    # last_withdraw = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)

    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def referral_profit(self):
        qs = Referral.objects.filter(user=self.user).first()
        if qs:
            return qs.total_referral_income
        return None

    @property
    def total_profit(self):
        sum_amt = 0.00
        if self.company_profit:
            print('aaaaa', self.referral_profit)
            print('ccccc', self.company_profit)
            sum_amt = self.referral_profit + self.company_profit
        else:
            sum_amt = self.referral_profit
        print('dddddd', sum_amt)
        return sum_amt

    @property
    def total_withdraw(self):
        sum_amt = 0.00
        # qs = Withdraw.objects.filter(user=self.user)
        qs = self.withdraw_wallet.all()
        for i in qs:
            sum_amt += i.withdraw_balance
        return sum_amt

    # @property
    # def last_month_profit(self):
    #     qs = Referral.objects.filter(user=self.user).annotate(month=TruncMonth(''))

    def __str__(self):
        return str(self.user)


def post_save_create_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance)


post_save.connect(post_save_create_wallet, sender=User)


def pre_save_company_profit_with_referral_report(sender, instance, **kwargs):
    obj = sender.objects.filter(pk=instance.pk)
    if obj.exists():
        obj = obj.first()
        if not obj.company_profit == instance.company_profit:  # Field has changed
            ref_rep = ReferralReport.objects.filter(user=instance.user)
            if ref_rep.exists():
                ref_rep = ref_rep.last()
                print(ref_rep.Date, localtime(now()).month)
                if ref_rep.Date.month == localtime(now()).month:
                    ref_rep.company_profit = instance.company_profit
                    ref_rep.save()
                else:
                    ReferralReport.objects.create(user=instance.user, Date=localtime(now()).date(),
                                                  company_profit=instance.company_profit)
    else:
        ReferralReport.objects.create(user=instance.user, Date=localtime(now()))


pre_save.connect(pre_save_company_profit_with_referral_report, sender=Wallet)

# def post_save_balance_with_company_profit(sender, instance, **kwargs):
#     print('enterrrrrrrrrrrrrrrrrrr')
#     obj = sender.objects.filter(pk=instance.pk).first()
#     if not obj.company_profit == instance.company_profit:  # Field has changed
#         instance.balance =
#     if instance.company_profit or obj.balance:
#         print('22222222222')
#         print(instance.company_profit + instance.referral_profit)
#         instance.balance += instance.company_profit
#
# pre_save.connect(post_save_balance_with_company_profit, sender=Wallet)

# def post_save_balance(sender, instance, created, **kwargs):
#     qs = Wallet.objects.filter(user=instance.user).first()
#     qs.balance = qs.total_profit
#     qs.save()
#
# post_save.connect(post_save_balance, sender=Referral)
