from django.contrib import admin
from .models import User, UserDetails, EFranchiseInfo, EHubInfo, UserAddress, ActiveAccount, ResetPassword, \
    EHubReport, EHubPurchasePerson, FranchiseUserNewRequestProxyModel, HubUserNewRequestProxyModel, \
    FranchiseNewUserProxyModel, HubNewUserProxyModel


# Register your models here.

class EFranchiseInfoInline(admin.TabularInline):
    model = EFranchiseInfo
    extra = 0


class FranchiseUserNewRequestProxyAdmin(admin.ModelAdmin):
    inlines = [EFranchiseInfoInline]
    # inlines = (EFranchiseInfoInline,)
    list_display = ['first_name', 'last_name', 'email', 'phone_number', 'is_active']
    fields = ['first_name', 'last_name', 'email', 'phone_number', 'role', 'is_confirmed', 'is_blocked',
              'is_active', 'is_staff']
    search_fields = ['email', 'phone_number']
    list_filter = ['email', 'phone_number']
    list_editable = ['is_active']

    class Meta:
        model = FranchiseUserNewRequestProxyModel

    def get_queryset(self, request):
        return FranchiseUserNewRequestProxyModel.objects.filter(role="FRANCHISE", is_active=False)


admin.site.register(FranchiseUserNewRequestProxyModel, FranchiseUserNewRequestProxyAdmin)


class EHubInfoInline(admin.TabularInline):
    model = EHubInfo
    extra = 0


class HubUserNewRequestProxyAdmin(admin.ModelAdmin):
    inlines = [EHubInfoInline]
    list_display = ['first_name', 'last_name', 'email', 'phone_number', 'is_active']
    fields = ['first_name', 'last_name', 'email', 'phone_number', 'role', 'is_confirmed', 'is_blocked',
              'is_active', 'is_staff']
    search_fields = ['email', 'phone_number']
    list_filter = ['email', 'phone_number']
    list_editable = ['is_active']

    class Meta:
        model = HubUserNewRequestProxyModel

    def get_queryset(self, request):
        return HubUserNewRequestProxyModel.objects.filter(role="HUB", is_active=False)


admin.site.register(HubUserNewRequestProxyModel, HubUserNewRequestProxyAdmin)


class FranchiseNewUserProxyAdmin(admin.ModelAdmin):
    inlines = [EFranchiseInfoInline]
    # inlines = (EFranchiseInfoInline,)
    list_display = ['first_name', 'last_name', 'email', 'phone_number', 'is_active']
    fields = ['first_name', 'last_name', 'email', 'phone_number', 'role', 'is_confirmed', 'is_blocked',
              'is_active', 'is_staff']
    search_fields = ['email', 'phone_number']
    list_filter = ['email', 'phone_number']
    list_editable = ['is_active']

    class Meta:
        model = FranchiseNewUserProxyModel

    def get_queryset(self, request):
        return FranchiseNewUserProxyModel.objects.filter(role="FRANCHISE", is_active=True)


admin.site.register(FranchiseNewUserProxyModel, FranchiseNewUserProxyAdmin)


class HubNewUserProxyAdmin(admin.ModelAdmin):
    inlines = [EHubInfoInline]
    # inlines = (EFranchiseInfoInline,)
    list_display = ['first_name', 'last_name', 'email', 'phone_number', 'is_active']
    fields = ['first_name', 'last_name', 'email', 'phone_number', 'role', 'is_confirmed', 'is_blocked',
              'is_active', 'is_staff']
    search_fields = ['email', 'phone_number']
    list_filter = ['email', 'phone_number']
    list_editable = ['is_active']

    class Meta:
        model = HubNewUserProxyModel

    def get_queryset(self, request):
        return HubNewUserProxyModel.objects.filter(role="HUB", is_active=True)


admin.site.register(HubNewUserProxyModel, HubNewUserProxyAdmin)


class UserDetailsInline(admin.TabularInline):
    model = UserDetails
    extra = 0


class UserAdmin(admin.ModelAdmin):
    inlines = [UserDetailsInline]
    list_display = ['first_name', 'last_name', 'email', 'phone_number', 'is_active']
    fields = ['first_name', 'last_name', 'email', 'phone_number', 'role', 'is_confirmed', 'is_blocked',
              'is_active', 'is_staff']
    search_fields = ['email', 'phone_number']
    list_filter = ['email', 'phone_number']
    list_editable = ['is_active']

    class Meta:
        model = User


admin.site.register(User, UserAdmin)

admin.site.register(UserDetails)


class EFranchiseInfoAdmin(admin.ModelAdmin):
    list_display = ['user', 'three_years_store_number', 'five_years_store_number', 'status']
    search_fields = ['user']
    list_filter = ['user']

    class Meta:
        model = EFranchiseInfo


admin.site.register(EFranchiseInfo, EFranchiseInfoAdmin)


class EHubInfoAdmin(admin.ModelAdmin):
    list_display = ['user', 'space_type', 'space_description', 'contact_year', 'status']
    search_fields = ['user']
    list_filter = ['user']

    class Meta:
        model = EHubInfo


admin.site.register(EHubInfo, EHubInfoAdmin)

admin.site.register(EHubReport)

admin.site.register(UserAddress)

admin.site.register(ActiveAccount)

admin.site.register(ResetPassword)


class EHubPurchasePersonAdmin(admin.ModelAdmin):
    list_display = ['get_hub_owner', 'person_name', 'person_email', 'number_of_sells_product', 'total_amount_of_sells_product']
    search_fields = ['person_name']
    list_filter = ['person_name']

    @admin.display(description='Hub Owner')
    def get_hub_owner(self, obj):
        return obj.hub.user.first_name

    class Meta:
        model = EHubPurchasePerson


admin.site.register(EHubPurchasePerson, EHubPurchasePersonAdmin)
