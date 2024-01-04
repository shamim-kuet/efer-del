from rest_framework.serializers import ModelSerializer
from .models import Country, Address, FranchiseMeta, ContentSettings, GeneralSettings, ContactUs, HowThisWorkSettings
from user.models import User
from user.serializers import EHubDetailsSerializer


class CountrySerializer(ModelSerializer):

    class Meta:
        model = Country
        fields = ['id', 'name']


class AddressSerializer(ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'address', 'is_hired']


class HubAddressSerializer(ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'address', 'full_address', 'office_address']


class HubUserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name']


class AddressMapSerializer(ModelSerializer):
    hub_user = HubUserSerializer(read_only=True)

    class Meta:
        model = Address
        fields = ['id', 'hub_user', 'office_address', 'address', 'lat', 'lng', 'is_hub', 'country', 'is_hired', 'population']


class AvailableAddressSerializer(ModelSerializer):
    hub_info = EHubDetailsSerializer(read_only=True)

    class Meta:
        model = Address
        fields = ['id', 'address', 'office_address', 'country', 'hub_info']


class FranchiseMetaSerializer(ModelSerializer):
    class Meta:
        model = FranchiseMeta
        fields = ['id', 'three_years_store_price', 'five_years_store_price']


class HowThisWorkSettingsSerializer(ModelSerializer):
    class Meta:
        model = HowThisWorkSettings
        fields = ['id', 'intro', 'business_strategy', 'goodKnow', 'youtube_video_link']


class TermsSerializer(ModelSerializer):
    class Meta:
        model = ContentSettings
        fields = ['id', 'terms']


class PrivacySerializer(ModelSerializer):
    class Meta:
        model = ContentSettings
        fields = ['id', 'privacy_policy']


class SiteMetaSerializer(ModelSerializer):
    class Meta:
        model = GeneralSettings
        fields = ['id', 'website_name', 'website_icon1', 'website_icon2', 'website_email', 'website_address',
                  'website_phone']

class SiteSocialLinkMetaSerializer(ModelSerializer):
    class Meta:
        model = GeneralSettings
        fields = ['id', 'facebook_url', 'twitter_url', 'instagram_url', 'youtube_url', 'linkedIn_url']


class ContactUsSerializer(ModelSerializer):
    class Meta:
        model = ContactUs
        fields = ['id', 'name', 'email', 'phone', 'query']