from django.db import models
from tinymce.models import HTMLField
from geopy.geocoders import GoogleV3
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from user.models import User, EHubInfo, UserDetails, HubUserNewRequestProxyModel

APIKEY = settings.GOOGLE_PLACES_API


class Country(models.Model):
    name = models.CharField(max_length=50)

    status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Address(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='country_address')
    hub_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ehub_user_address',
                                 null=True, blank=True, help_text="Please don't fill this field when creating address")
    hub_info = models.ForeignKey(EHubInfo, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='address_hub_info')
    full_address = models.CharField(max_length=255, blank=True, null=True)

    address = models.CharField(max_length=100)

    population = models.CharField(max_length=255, null=True, blank=True)

    office_address = models.CharField(max_length=255, null=True, blank=True)

    lat = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True)
    lng = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True)


    is_hub = models.BooleanField(default=False)
    is_hired = models.BooleanField(default=False, help_text="Please don't fill this field when creating address")

    status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.full_address:
            geolocator2 = GoogleV3(api_key=APIKEY)
            location2 = geolocator2.geocode(
                self.full_address, timeout=10)
            if location2:
                self.lat = location2.latitude
                self.lng = location2.longitude

        return super(Address, self).save(*args, **kwargs)

    def __str__(self):
        return self.address


class HubAddressProxyModel(Address):

    class Meta:
        verbose_name = ' E-Hub Address'
        verbose_name_plural = ' E-Hub Address'
        proxy = True


class EFranchiseAddressProxyModel(Address):

    class Meta:
        verbose_name = ' E-Franchise Address'
        verbose_name_plural = ' E-Franchise Address'
        proxy = True


class PostCode(models.Model):
    hub_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='hub_post_code')
    name = models.CharField(max_length=255, blank=True, null=True)

    status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class FranchiseMeta(models.Model):
    three_years_store_price = models.IntegerField(null=True, blank=True)
    five_years_store_price = models.IntegerField(null=True, blank=True)


class GeneralSettings(models.Model):
    website_name = models.CharField(max_length=100)
    website_icon1 = models.ImageField(upload_to='photos/meta/webicon1/%Y/%m/%d/', null=True, blank=True)
    website_icon2 = models.ImageField(upload_to='photos/meta/webicon2/%Y/%m/%d/', null=True, blank=True)
    website_email = models.EmailField(max_length=100, null=True, blank=True)
    website_address = models.TextField(null=True, blank=True)
    website_phone = models.CharField(max_length=50, null=True, blank=True)
    facebook_url = models.URLField(null=True, blank=True)
    twitter_url = models.URLField(null=True, blank=True)
    instagram_url = models.URLField(null=True, blank=True)
    youtube_url = models.URLField(null=True, blank=True)
    linkedIn_url = models.URLField(null=True, blank=True)

    status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.website_name

    class Meta:
        verbose_name = 'General Settings'
        verbose_name_plural = 'General Settings'


class ContentSettings(models.Model):
    terms = HTMLField(null=True, blank=True)
    privacy_policy = HTMLField(null=True, blank=True)

    status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Content Settings'
        verbose_name_plural = 'Content Settings'


class HowThisWorkSettings(models.Model):
    intro = HTMLField(null=True, blank=True)
    business_strategy = HTMLField(null=True, blank=True)
    goodKnow = HTMLField(null=True, blank=True)
    youtube_video_link = models.URLField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'How This Work'
        verbose_name_plural = 'How This Work'


class ContactUs(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    query = models.TextField(null=True, blank=True)

    status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Contact US'
        verbose_name_plural = 'Contact US'


@receiver(post_save, sender=HubUserNewRequestProxyModel)
def assign_address_ehub_user(sender, instance, created, **kwargs):
    print('enterrrrrr1111111111111')
    print(instance.role)
    print(instance.is_active)
    if instance.role == 'HUB' and instance.is_active == True:
        print('enterrrrrr222222222')
        user_details_qs = UserDetails.objects.filter(user=instance)
        print('user_details_qs', user_details_qs)
        if user_details_qs:
            user_details_qs = user_details_qs.first()
            qs = EHubInfo.objects.filter(user=instance)
            print('qs', qs)
            if qs.exists():
                qs = qs.first()
                address_qs = Address.objects.filter(pk=int(user_details_qs.requested_hub))
                print('address_qs', address_qs)
                if address_qs.exists():
                    address_qs = address_qs.first()
                    address_qs.hub_user = instance
                    address_qs.hub_info = qs
                    address_qs.office_address = qs.office_location
                    address_qs.is_hired = True
                    address_qs.save()

@receiver(pre_save, sender=User)
def assign_address_ehub_user_model(sender, instance, **kwargs):
    print(instance.role)
    print(instance.is_active)
    if instance.role == 'HUB' and instance.is_active == False:
        user_details_qs = UserDetails.objects.filter(user=instance)
        if user_details_qs:
            user_details_qs = user_details_qs.first()
            qs = EHubInfo.objects.filter(user=instance)
            if qs.exists():
                qs = qs.first()
                address_qs = Address.objects.filter(pk=int(user_details_qs.requested_hub))
                if address_qs.exists():
                    address_qs = address_qs.first()
                    address_qs.hub_user = instance
                    address_qs.hub_info = qs
                    address_qs.office_address = qs.office_location
                    address_qs.is_hired = True
                    address_qs.save()

        # qs = EHubInfo.objects.filter(user=instance)
        # if qs.exists():
        #     qs = qs.first()
        #     address_qs = Address.objects.filter(hub_user=qs)
        #     if address_qs.exists():
        #         address_qs = address_qs.first()
        #         address_qs.office_address = qs.office_location
        #         address_qs.is_hired = True
        #         address_qs.save()
