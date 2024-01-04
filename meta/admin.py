from django.contrib import admin
from .models import Country, Address, FranchiseMeta, ContentSettings, ContactUs, HowThisWorkSettings, GeneralSettings,\
    PostCode, HubAddressProxyModel, EFranchiseAddressProxyModel

# Register your models here.
class PostCodeInline(admin.TabularInline):
    model = PostCode


class AddressAdmin(admin.ModelAdmin):
    list_display = ['country', 'hub_user', 'address', 'population', 'is_hub', 'is_hired', 'post_code']
    list_filter = ['address', 'is_hub', 'is_hired']
    search_fields = ['address']
    inlines = [PostCodeInline]
    list_editable = ['is_hub', 'is_hired']
    fieldsets = (
        ('Admin Editable', {'fields': ('country', 'full_address', 'address', 'population', 'is_hub')}),
        ('Map info', {'fields': ('lat', 'lng')}),
        ('Information', {'fields': ('office_address', 'is_hired', 'status',)}),
    )

    def post_code(self, obj):
        return ",".join([k.name for k in obj.hub_post_code.all()])

    # def post_code(self, obj):
    #     return obj.hub_post_code.all()


admin.site.register(Address, AddressAdmin)

class HubAddressProxyModelAdmin(admin.ModelAdmin):
    list_display = ['country', 'hub_user', 'address', 'population', 'is_hub', 'is_hired', 'post_code']
    list_filter = ['address', 'is_hub', 'is_hired']
    search_fields = ['address']
    inlines = [PostCodeInline]
    list_editable = ['is_hub', 'is_hired']
    fieldsets = (
        ('Admin Editable', {'fields': ('country', 'full_address', 'address', 'population', 'is_hub')}),
        ('Map info', {'fields': ('lat', 'lng')}),
        ('Information', {'fields': ('hub_user', 'hub_info', 'office_address', 'is_hired', 'status',)}),
    )

    def post_code(self, obj):
        return ",".join([k.name for k in obj.hub_post_code.all()])

    def get_queryset(self, request):
        return HubAddressProxyModel.objects.filter(is_hub=True)

admin.site.register(HubAddressProxyModel, HubAddressProxyModelAdmin)

class EFranchiseAddressProxyModelAdmin(admin.ModelAdmin):
    list_display = ['country', 'address', 'post_code']
    list_filter = ['address', 'is_hired']
    search_fields = ['address']
    inlines = [PostCodeInline]
    fieldsets = (
        ('Admin Editable', {'fields': ('country', 'full_address', 'address')}),
        ('Map info', {'fields': ('lat', 'lng')}),
        ('Information', {'fields': ('status',)}),
    )

    def post_code(self, obj):
        return ",".join([k.name for k in obj.hub_post_code.all()])

    def get_queryset(self, request):
        return EFranchiseAddressProxyModel.objects.filter(is_hub=False)


admin.site.register(EFranchiseAddressProxyModel, EFranchiseAddressProxyModelAdmin)

admin.site.register(Country)
admin.site.register(FranchiseMeta)
admin.site.register(ContentSettings)
admin.site.register(GeneralSettings)
admin.site.register(ContactUs)
admin.site.register(HowThisWorkSettings)
