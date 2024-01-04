from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Country, Address, FranchiseMeta, ContentSettings, GeneralSettings, ContactUs, HowThisWorkSettings
from .serializers import CountrySerializer, AddressSerializer, FranchiseMetaSerializer,\
    PrivacySerializer, TermsSerializer, SiteMetaSerializer, SiteSocialLinkMetaSerializer, HowThisWorkSettingsSerializer,\
    AddressMapSerializer, AvailableAddressSerializer, HubAddressSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework.filters import BaseFilterBackend
import coreapi
from user.models import EHubInfo, EHubPurchasePerson
from django.utils.timezone import localtime, now
from django.db.models import Q


class SimpleFilterBackend(BaseFilterBackend):
    def get_schema_fields(self, view):
        return [coreapi.Field(
            name='country',
            location='query',
            required=False,
            type='string'
        )]


class GetAllCountryApiView(APIView):
    """ Get All Country Name """

    @swagger_auto_schema(responses={200: CountrySerializer(many=True)})
    def get(self, request):
        qs = Country.objects.all()
        serializer = CountrySerializer(qs, many=True)
        return Response(serializer.data)


class GetAddressByCountryApiView(APIView):
    """ Get All Address By Country Name """
    filter_backends = (SimpleFilterBackend,)

    # @swagger_auto_schema(
    #     # methods=['GET'],
    #     operation_description="GET All Country Address",
    #     # request_body=openapi.Schema(
    #     #     type=openapi.TYPE_OBJECT,
    #     #     required=['category', 'name', 'location', 'start_date', 'end_date', 'description', 'completed', 'banner'],
    #     #     properties={
    #     #         'category': openapi.Schema(type=openapi.TYPE_STRING),
    #     #         'name': openapi.Schema(type=openapi.TYPE_STRING),
    #     #         'location': openapi.Schema(type=openapi.TYPE_STRING),
    #     #         'start_date': openapi.Schema(type=openapi.TYPE_STRING, default="yyyy-mm-dd"),
    #     #         'end_date': openapi.Schema(type=openapi.TYPE_STRING, default='yyyy-mm-dd'),
    #     #         'description': openapi.Schema(type=openapi.TYPE_STRING),
    #     #         'completed': openapi.Schema(type=openapi.TYPE_BOOLEAN, default=False),
    #     #         'banner': openapi.Schema(type=openapi.TYPE_FILE),
    #     #     },
    #     # ),
    # )
    @swagger_auto_schema(responses={200: AddressSerializer(many=True)})
    def get(self, request):
        country = request.query_params.get('country')
        country_qs = Country.objects.filter(pk=country)
        if country_qs.exists():
            country_qs = country_qs.first()
            addr_qs = Address.objects.filter(country=country_qs, is_hub=True)
            serializer = AddressSerializer(addr_qs, many=True)
            return Response(serializer.data)


class GetFranchiseAddressByCountryFilterBackend(BaseFilterBackend):
    def get_schema_fields(self, view):
        return [coreapi.Field(
            name='country',
            location='query',
            required=False,
            type='string'
        )]


class GetFranchiseAddressByCountryApiView(APIView):
    filter_backends = (GetFranchiseAddressByCountryFilterBackend,)

    @swagger_auto_schema(responses={200: AddressSerializer(many=True)},
                         operation_description="GET E-Franchise Address By Country Name")
    def get(self, request):
        country = request.query_params.get('country', 2)
        country_qs = Country.objects.filter(pk=country)
        if country_qs.exists():
            country_qs = country_qs.first()
            addr_qs = Address.objects.filter(country=country_qs, is_hub=False)
            serializer = AddressSerializer(addr_qs, many=True)
            return Response(serializer.data)


class FranchiseMetaAPIView(APIView):

    @swagger_auto_schema(responses={200: FranchiseMetaSerializer()},
                         operation_description="Get E-Franchise Store Price")
    def get(self, request):
        qs = FranchiseMeta.objects.all()
        serializer = FranchiseMetaSerializer(qs.first())
        return Response(serializer.data)


class HowThisWorkAPIView(APIView):

    @swagger_auto_schema(responses={200: HowThisWorkSettingsSerializer()},
                         operation_description="Get How This Work Page Information")
    def get(self, request):
        qs = HowThisWorkSettings.objects.all()
        serializer = HowThisWorkSettingsSerializer(qs.last())
        return Response(serializer.data)


class PrivacyAPIView(APIView):

    @swagger_auto_schema(responses={200: PrivacySerializer()},
                         operation_description="Get Privacy Policy Page Information")
    def get(self, request):
        qs = ContentSettings.objects.filter(status=True)
        serializer = PrivacySerializer(qs.first())
        return Response(serializer.data)


class TermsAPIView(APIView):

    @swagger_auto_schema(responses={200: TermsSerializer()},
                         operation_description="Get Terms and Condition Page Information")
    def get(self, request):
        qs = ContentSettings.objects.filter(status=True)
        serializer = TermsSerializer(qs.first())
        return Response(serializer.data)


class SiteMetaAPIView(APIView):

    @swagger_auto_schema(responses={200: SiteMetaSerializer()}, operation_description="Get Site Meta Data Information")
    def get(self, request):
        qs = GeneralSettings.objects.filter(status=True)
        serializer = SiteMetaSerializer(qs.first())
        return Response(serializer.data)


class SiteSocialLinkMetaAPIView(APIView):

    @swagger_auto_schema(responses={200: SiteSocialLinkMetaSerializer()},
                         operation_description="Get Site Social Link Information")
    def get(self, request):
        qs = GeneralSettings.objects.filter(status=True)
        serializer = SiteSocialLinkMetaSerializer(qs.first())
        return Response(serializer.data)


class ContactUsApiview(APIView):

    @swagger_auto_schema(
        # methods=['GET'],
        operation_description="Post user contact information",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name', 'email', 'phone', 'query'],
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'phone': openapi.Schema(type=openapi.TYPE_STRING),
                'query': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={200: 'success'}
    )
    def post(self, request):
        data = request.data
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        query = data.get('query')
        ContactUs.objects.create(
            name=name,
            email=email,
            phone=phone,
            query=query,
        )
        return Response({'message': 'success'})


class MapApiView(APIView):

    @swagger_auto_schema(responses={200: AddressMapSerializer(many=True)},
                         operation_description="Get Find BMP Page Information")
    def get(self, request):
        qs = Address.objects.filter(lng__isnull=False, is_hub=True).select_related("hub_user")
        serializer = AddressMapSerializer(qs, many=True)
        return Response(serializer.data)


class AvailableHubApiView(APIView):

    @swagger_auto_schema(responses={200: AddressMapSerializer(many=True)},
                         operation_description="Get All Available Hub")
    def get(self, request):
        search_code = request.query_params.get('search_code', "")
        search_area = request.query_params.get('search_area', "")
        # if search_code and search_area:
        #     qs = Address.objects.filter(Q(hub_post_code__name__icontains=search_code) and Q(full_address__icontains=search_area),
        #                                 is_hub=True).distinct()[:6]
        #     if not qs.exists():
        #         qs = Address.objects.filter(lng__isnull=False, is_hub=True)[:6]
        if search_code:
            qs = Address.objects.filter(lng__isnull=False, is_hub=True,
                                        hub_post_code__name__icontains=search_code
                                        ).select_related('hub_info').prefetch_related('hub_info__user')[:10]
            if not qs.exists() and search_area:
                qs = Address.objects.filter(lng__isnull=False, is_hub=True,
                                            full_address__icontains=search_area
                                            ).select_related('hub_info').prefetch_related('hub_info__user')[:10]
            if qs.count() == 0:
                qs = Address.objects.filter(lng__isnull=False, is_hub=True
                                            ).select_related('hub_info').prefetch_related('hub_info__user')[:10]
        elif search_area:
            qs = Address.objects.filter(lng__isnull=False, is_hub=True,
                                        full_address__icontains=search_area
                                        ).select_related('hub_info').prefetch_related('hub_info__user')[:10]
        else:
            qs = Address.objects.filter(lng__isnull=False, is_hub=True
                                        ).select_related('hub_info').prefetch_related('hub_info__user')[:10]

        serializer = AvailableAddressSerializer(qs, many=True)
        return Response(serializer.data)


class SingleHubDetails(APIView):
    def get(self, request, pk):
        address = Address.objects.filter(hub_info=pk, is_hub=True)
        if address.exists():
            address = address.first()
            serializer = HubAddressSerializer(address, many=False)
            return Response(serializer.data)
        return Response({
            "message": "No Hub Found"
        })


class OwnHubApiView(APIView):
    @swagger_auto_schema(
        # methods=['GET'],
        operation_description="Your Own Hub Info (AUTHENTICATED)",
    )
    def get(self, request):
        qs = Address.objects.filter(Q(lng__isnull=False) and Q(hub_user=request.user))
        if qs.exists():
            qs = qs.first()
            serializer = AddressMapSerializer(qs)
            return Response(serializer.data)
        return Response({"message": "No hub found"})


class EHubPurchasePersonApiView(APIView):

    # @swagger_auto_schema(responses={200: HowThisWorkSettingsSerializer()})
    @swagger_auto_schema(
        # methods=['POST'],
        operation_description="POST HUB ADDRESS",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['hub_post_code', 'order_amount', 'number_of_product', 'person_name', 'person_email',
                      'invoice_file', 'person_id'],
            properties={
                'hub_post_code': openapi.Schema(type=openapi.TYPE_STRING),
                'order_amount': openapi.Schema(type=openapi.TYPE_STRING),
                'number_of_product': openapi.Schema(type=openapi.TYPE_STRING),
                'person_name': openapi.Schema(type=openapi.TYPE_STRING),
                'person_email': openapi.Schema(type=openapi.TYPE_STRING),
                'invoice_file': openapi.Schema(type=openapi.TYPE_STRING),
                'person_id': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
    )
    def post(self, request):
        data = request.data
        hub_code = data.get('hub_post_code')
        split_code = hub_code.split()[0]
        order_amount = data.get('order_amount')
        number_of_product = data.get('number_of_product')
        person_name = data.get('person_name')
        person_email = data.get('person_email')
        invoice_file = data.get('invoice_file')
        person_id = data.get('person_id')

        address = Address.objects.filter(hub_post_code__name__exact=split_code)
        if address.exists():
            address = address.first()
        else:
            return Response({"message": "Address not found"})

        hub_qs = EHubInfo.objects.filter(address_hub_info=address)
        if hub_qs.exists():
            hub_qs = hub_qs.first()
            EHubPurchasePerson.objects.create(hub=hub_qs, person_name=person_name, person_email=person_email,
                                              person_id=person_id,
                                              number_of_sells_product=number_of_product,
                                              total_amount_of_sells_product=order_amount,
                                              invoice=invoice_file, Date=localtime(now()).date())
            # hub_report_qs = EHubReport.objects.filter(hub=hub_qs)
            # if hub_report_qs.exists():
            #     hub_report_qs = hub_report_qs.first()
            #     if hub_report_qs.Date.month == localtime(now()).month:
            #         hub_report_qs.number_of_sells_product = int(hub_report_qs.number_of_sells_product) + \
            #                                                 int(number_of_product)
            #         hub_report_qs.total_amount_of_sells_product = \
            #             float(hub_report_qs.total_amount_of_sells_product) \
            #             + float(order_amount)
            #
            #         hub_report_qs.save()
            #     else:
            #         EHubReport.objects.create(hub=hub_qs, Date=localtime(now()).date(),
            #                                   number_of_sells_product=number_of_product,
            #                                   total_amount_of_sells_product=order_amount)
            # else:
            #     EHubReport.objects.create(hub=hub_qs, Date=localtime(now()).date(),
            #                               number_of_sells_product=number_of_product,
            #                               total_amount_of_sells_product=order_amount)
            return Response({"message": "EHub Person Added Successfully"})
        return Response({"message": "EHub Not Found"})
