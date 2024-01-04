from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.validators import UnicodeUsernameValidator


class UserManager(BaseUserManager):
    def create_user(self, email=None, phone_number=None, password=None, **kwargs):
        user = self.model(email=self.normalize_email(email),
                          phone_number=phone_number, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, phone_number=None, password=None, **kwargs):
        user = self.model(email=self.normalize_email(email),
                          phone_number=phone_number, is_staff=True,
                          is_superuser=True, is_active=True, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user




roleType = [
    ('FRANCHISE', 'Franchise'),
    ('HUB', 'Hub'),
]

class StrippedCharField(models.CharField):
    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        if value is not None:
            value = value.strip()
        return value


class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(_('username'), max_length=255, help_text=_('Required. 255 characters or fewer. '
                                                                           'Letters, digits and @/./+/-/_ only.'),
                                validators=[username_validator], unique=True, null=True, blank=True
                                )
    first_name = StrippedCharField(max_length=225, null=True, blank=True)
    last_name = models.CharField(max_length=225, null=True, blank=True)

    email = models.EmailField(
        _('email address'), unique=True, null=True, blank=True)
    phone_number = models.CharField(
        _('phone number'), max_length=255, null=True, blank=True)
    role = models.CharField(choices=roleType, max_length=255, default='USER')
    is_confirmed = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # def clean(self):
    #     if self.first_name:
    #         print('aaaaaaaa')
    #         self.first_name = self.first_name.strip()
    #         print('bbbbbb', self.first_name)
    #
    # def save(self, *args, **kwargs):
    #     self.clean()
    #     return super(User, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.email)

    class Meta:
        verbose_name = '   User'
        verbose_name_plural = '   Users'



class FranchiseUserNewRequestProxyManager(UserManager):
    def all(self):
        return self.get_queryset().filter(role="FRANCHISE", is_active=True)


class FranchiseUserNewRequestProxyModel(User):
    objects = FranchiseUserNewRequestProxyManager()

    class Meta:
        verbose_name = '      E-Franchise User Request'
        verbose_name_plural = '      E-Franchise User Requests'
        proxy = True


class HubUserNewRequestProxyManager(UserManager):
    def all(self):
        return self.get_queryset().filter(role="HUB", is_active=True)


class HubUserNewRequestProxyModel(User):
    objects = HubUserNewRequestProxyManager()

    class Meta:
        verbose_name = '     E-Hub User Request'
        verbose_name_plural = '     E-Hub User Requests'
        proxy = True


class FranchiseNewUserProxyModel(User):

    class Meta:
        verbose_name = '   E-Franchise User'
        verbose_name_plural = '   E-Franchise Users'
        proxy = True


class HubNewUserProxyModel(User):

    class Meta:
        verbose_name = '   E-Hub User'
        verbose_name_plural = '   E-Hub Users'
        proxy = True



class UserDetails(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='user_details', blank=True, null=True)

    profile_pic = models.ImageField(
        upload_to='photos/profile_pic/%Y/%m/%d/', null=True, blank=True)

    imp_doc = models.FileField(upload_to='file/imp_doc/%Y/%m/%d/', null=True, blank=True)
    citizen = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    requested_hub = models.CharField(max_length=25, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = '  User Details'
        verbose_name_plural = '  User Details'


class EFranchiseInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_franchise', blank=True, null=True)
    three_years_store_number = models.IntegerField(null=True, blank=True)
    five_years_store_number = models.IntegerField(null=True, blank=True)
    total_liquid_assets = models.CharField(max_length=255, null=True, blank=True)
    total_net_worth = models.CharField(max_length=255, null=True, blank=True)

    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)

    bank_statement = models.FileField(upload_to='file/bank_statement/%Y/%m/%d/', null=True, blank=True)

    status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = ' EFranchise Info'
        verbose_name_plural = ' EFranchise Info'


spaceType = [
    ('FEET', 'Squire Feet'),
    ('FLOOR', 'Floor'),
]


class EHubInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_hub', blank=True, null=True)
    space_type = models.CharField(choices=spaceType, max_length=20, null=True, blank=True)
    space_description = models.TextField(null=True, blank=True)
    office_location = models.CharField(max_length=255, null=True, blank=True)
    space_img = models.ImageField(upload_to='photos/ehub_pic/%Y/%m/%d/', null=True, blank=True)
    space_video = models.FileField(upload_to='video/ehub_pic/%Y/%m/%d/', null=True, blank=True)
    available_from = models.DateTimeField(null=True, blank=True)
    is_delivery_man = models.BooleanField(default=False)
    delivery_vehicles = models.CharField(max_length=20, null=True, blank=True)

    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)

    contact_year = models.IntegerField(null=True, blank=True)

    status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = ' EHub Info'
        verbose_name_plural = ' EHub Info'


class EHubPurchasePerson(models.Model):
    hub = models.ForeignKey(EHubInfo, on_delete=models.CASCADE, related_name='purchase_person')
    person_name = models.CharField(max_length=50)
    person_id = models.CharField(max_length=50)
    person_email = models.EmailField(max_length=50, null=True, blank=True)
    number_of_sells_product = models.IntegerField(default=0)
    total_amount_of_sells_product = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    invoice = models.URLField(max_length=500, null=True, blank=True)

    active = models.BooleanField(default=True)

    Date = models.DateField(null=True, blank=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return self.referred_person_name


class EHubReport(models.Model):
    hub = models.ForeignKey(EHubInfo, on_delete=models.CASCADE, related_name='profit_report')
    Date = models.DateField(null=True, blank=False)
    number_of_sells_product = models.IntegerField(default=0)
    total_amount_of_sells_product = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)

    active = models.BooleanField(default=True)

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

    def __str__(self):
        return str(self.hub)


class UserAddress(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_address', blank=True, null=True)

    eHubAddress = models.ForeignKey(EHubInfo, on_delete=models.CASCADE, related_name='ehub_address',
                                    null=True, blank=True)

    eFranchiseAddress = models.ForeignKey(EFranchiseInfo, on_delete=models.CASCADE, related_name='efranchise_address',
                                          null=True, blank=True)

    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    postcode = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    others = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = ' Address'
        verbose_name_plural = ' Address'


    def __str__(self):
        return str(self.user)


class ActiveAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='active_account')
    uuid = models.CharField(max_length=255)
    expire_time = models.DateTimeField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.uuid


class ResetPassword(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reset_password')
    uuid = models.CharField(max_length=255)
    expire_time = models.DateTimeField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.uuid



