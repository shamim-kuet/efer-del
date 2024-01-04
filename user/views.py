import pytz
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from django.db.models import Q
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model
from django.utils.timezone import localtime, now
from .models import UserDetails, UserAddress, EHubInfo, EFranchiseInfo, ActiveAccount, EHubReport, ResetPassword, \
    EHubPurchasePerson
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import APIException
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from efranchise.utils import unique_uuid_generator, send_html_mail
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserWithProfileSerializer, ResetPasswordSerializer, ResetPasswordConfirmSerializer \
    , EHubShortSerializer, EHubPersonSerializer, EHubDetailsSerializer
from referral.models import ReferralReport
from django.db.models import Sum
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

User = get_user_model()


def validate_password(password):
    if len(password) < 8:
        raise APIException(_('Password length must be greater than 8 character.'))
    # if not re.findall('\d', password):
    #     raise APIException(_('The password must contain at least 1 digit, 0-9.'))
    # if not re.findall('[A-Z]', password):
    #     raise APIException(_('The password must contain at least 1 uppercase letter, A-Z.'))
    # if not re.findall('[a-z]', password):
    #     raise APIException(_('The password must contain at least 1 lowercase letter, a-z.'))
    return password


class RegistrationApiView(APIView):

    def post(self, request):
        data = request.data
        phone = data.get('phone')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role')
        print(role)
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        requested_hub = data.get('requested_hub')
        # new_user = user.objects.create(
        #     first_name=first_name, last_name=last_name,
        #     email=email, phone_number=phone, role=role
        # )
        if User.objects.filter(email=email).exists():
            return Response({"message": "User with this email already registered"}, status=status.HTTP_400_BAD_REQUEST)
        validation = validate_password(password=password)
        if validation == password:
            new_user = User.objects.create(
                first_name=first_name, last_name=last_name,
                email=email, phone_number=phone, role=role
            )
            new_user.set_password(password)
            new_user.save()

            imp_doc = data.get('imp_doc')
            profile_pic = data.get('profile_pic')
            print(profile_pic)
            citizen = data.get('citizen')
            address = data.get('address')
            try:
                UserDetails.objects.create(user=new_user, imp_doc=imp_doc, profile_pic=profile_pic,
                                           citizen=citizen, address=address, requested_hub=requested_hub)

                expire_time = timezone.now() + timedelta(hours=48)
                new_uuid = ActiveAccount.objects.create(**{
                    'user_id': new_user.id,
                    'expire_time': expire_time
                })
                uid = unique_uuid_generator(instance=new_uuid)
                ActiveAccount.objects.filter(user_id=new_user.id, active=True).exclude(id=new_uuid.id).update(
                    active=False)
                new_uuid.uuid = uid
                new_uuid.save()

                if role == 'FRANCHISE':
                    three_years_store_number = data.get('three_years_store_number')
                    five_years_store_number = data.get('five_years_store_number')
                    total_liquid_assets = data.get('total_liquid_assets')
                    total_net_worth = data.get('total_net_worth')
                    bank_statement = data.get('bank_statement')
                    e_franchise = EFranchiseInfo.objects.create(
                        user=new_user,
                        three_years_store_number=three_years_store_number,
                        five_years_store_number=five_years_store_number,
                        total_liquid_assets=total_liquid_assets, total_net_worth=total_net_worth,
                        bank_statement=bank_statement
                    )
                    country = data.get('country')
                    city = data.get('city')
                    # state = data.get('state')
                    UserAddress.objects.create(country=country, city=city, user=new_user,
                                               eFranchiseAddress=e_franchise)

                    try:
                        frontend_url = settings.FRONT_END_URL + "/auth/reset-password/?code={}".format(new_uuid.uuid)
                        html_template = render_to_string('email/active-account.html', context={'link': frontend_url,
                                                                                               'code': new_uuid.uuid})
                        send_html_mail(subject='Active Account', html_content=html_template,
                                       recipient_list=[new_user.email])
                        return Response({
                            'message': 'Email send successfully',
                            "user_id": new_user.id
                        }, status=status.HTTP_200_OK)
                    except Exception as e:
                        return Response({'message': 'Unable to send email'}, status=status.HTTP_400_BAD_REQUEST)

                    # return Response({
                    #     "message": "E-Franchise Registration Successfully"
                    # })

                elif role == 'HUB':
                    office_location = data.get('office_location')
                    space_type = data.get('space_type')
                    space_description = data.get('space_description')
                    space_img = data.get('space_img')
                    space_video = data.get('space_video')
                    available_from = data.get('available_from')
                    is_delivery_man = data.get('is_delivery_man')
                    delivery_vehicles = data.get('delivery_vehicles')
                    contact_year = data.get('contact_year')
                    # True if form.data.get("status") == "on" else False
                    e_hub = EHubInfo.objects.create(user=new_user, space_type=space_type,
                                                    office_location=office_location,
                                                    space_description=space_description,
                                                    space_img=space_img, space_video=space_video,
                                                    available_from=available_from,
                                                    is_delivery_man=True if is_delivery_man == "true" else False,
                                                    delivery_vehicles=delivery_vehicles,
                                                    contact_year=contact_year)

                    city = data.get('city')
                    others = data.get('others')
                    UserAddress.objects.create(user=new_user, eHubAddress=e_hub, city=city, others=others)

                    # state = data.get('state')
                    # address_qs = Address.objects.filter(pk=state)
                    # if address_qs.exists():
                    #     address_qs = address_qs.first()
                    #     address_qs.hub_user = e_hub
                    #     address_qs.save()

                    try:
                        frontend_url = settings.FRONT_END_URL + "/auth/active-account/?code={}".format(new_uuid.uuid)
                        html_template = render_to_string('email/active-account.html', context={'link': frontend_url,
                                                                                               'code': new_uuid.uuid})
                        send_html_mail(subject='Active Account', html_content=html_template,
                                       recipient_list=[new_user.email])
                        return Response({
                            'message': 'Email send successfully',
                            "user_id": new_user.id
                        }, status=status.HTTP_200_OK)
                    except Exception as e:
                        return Response({'message': 'Unable to send email'}, status=status.HTTP_400_BAD_REQUEST)
                    # return Response({
                    #     "message": "E-Hub Registration Successfully"
                    # })
            except Exception as e:
                print(e)
                new_user.delete()
                return Response({"message": "Registration Failed and check to fill up all required field"},
                                status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Registration Failed"})


class ResendActivationCode(APIView):
    def post(self, request):
        new_user_id = request.data.get('new_user_id')
        user = User.objects.filter(id=new_user_id)
        if user.exists():
            user = user.first()
            expire_time = timezone.now() + timedelta(hours=48)
            new_uuid = ActiveAccount.objects.create(**{
                'user_id': user.id,
                'expire_time': expire_time
            })
            uid = unique_uuid_generator(instance=new_uuid)
            ActiveAccount.objects.filter(user_id=user.id, active=True).exclude(id=new_uuid.id).update(active=False)
            new_uuid.uuid = uid
            new_uuid.save()
            try:
                frontend_url = settings.FRONT_END_URL + "/auth/active-account/?code={}".format(new_uuid.uuid)
                html_template = render_to_string('email/active-account.html', context={'link': frontend_url,
                                                                                       'code': new_uuid.uuid})
                send_html_mail(subject='Active Account', html_content=html_template,
                               recipient_list=[user.email])
                return Response({
                    'message': 'Email send successfully',
                    "user_id": new_user_id
                }, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'message': 'Unable to send email'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'User Not Found'}, status=status.HTTP_400_BAD_REQUEST)


class AccountConfirmApiView(APIView):
    # permission_classes = [AllowAny, ]
    # serializer_class = ResetPasswordConfirmSerializer

    def post(self, request):
        uuid = request.data.get('code')
        print(uuid)
        # reset_object = get_object_or_404(ActiveAccount, uuid=uuid, active=True)
        reset_object = ActiveAccount.objects.filter(uuid=uuid, active=True)
        # serializer = self.serializer_class(data=request.data)
        utc = pytz.UTC
        if reset_object.exists():
            reset_object = reset_object.first()
            if reset_object.expire_time.replace(tzinfo=utc) < timezone.now().replace(tzinfo=utc):
                reset_object.active = False
                return Response({"message": "Code has expired."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                reset_object.active = False
                reset_object.user.is_confirmed = True
                reset_object.user.save()
                reset_object.save()
                return Response({"message": "Account Active successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Code has expired or not found."}, status=status.HTTP_400_BAD_REQUEST)


class Login(CreateAPIView):
    queryset = User.objects.filter(is_active=True)

    @swagger_auto_schema(
        # methods=['POST'],
        operation_description="LOGIN USER",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['identifier', 'password'],
            properties={
                'identifier': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
    )
    def post(self, request):
        # email = request.data.get('email')
        # validator = check_email_address_validity(email)
        password = request.data.get('password')
        #
        # if validator:
        #     user_instance = get_object_or_404(User, email=email)
        # else:
        #     user_instance = User.objects.filter(phone_number=email).first()

        identifier = request.data.get('identifier')
        print(password, identifier)
        user_instance = User.objects.filter(
            Q(email=identifier) | Q(phone_number=identifier)).first()
        print(user_instance)

        if user_instance is not None:
            if user_instance.check_password(password):
                if user_instance.is_confirmed:
                    if user_instance.is_active:
                        # if user_instance.check_password(password):
                        # print(user_instance.check_password('password', password))
                        report_qs = ReferralReport.objects.filter(user=user_instance)
                        print(report_qs)
                        if not report_qs.exists():
                            ReferralReport.objects.create(user=user_instance, Date=localtime(now()).date(),
                                                          profit=0)
                        else:
                            print(report_qs.last().profit)
                            report_qs = report_qs.last()
                            if report_qs.Date.month != localtime(now()).month:
                                ReferralReport.objects.create(user=user_instance, Date=localtime(now()).date(),
                                                              profit=0)
                        refresh = RefreshToken.for_user(user_instance)
                        return Response(
                            {
                                'message': 'login successful',
                                'data': {
                                    'refresh': str(refresh),
                                    'access': str(refresh.access_token),
                                }
                            },
                            status=status.HTTP_201_CREATED
                        )
                    else:
                        return Response(
                            {
                                'message': 'Your Information is under processing. Please contact our support for more'
                                           ' information',
                            }, status=status.HTTP_400_BAD_REQUEST
                        )
                else:
                    return Response(
                        {
                            'message': 'Check Email to confirm your account',
                            "user_id": user_instance.id
                        }, status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    {
                        'message': 'Email/Phn or password not correct',
                    }, status=status.HTTP_400_BAD_REQUEST
                )

        else:
            return Response(
                {
                    'message': 'Email/Phn or password not correct',
                }, status=status.HTTP_400_BAD_REQUEST
            )


class UserApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        # serializer = UserSerializer(user)
        user_details = UserDetails.objects.filter(user=user).first()
        serializer = UserWithProfileSerializer(user_details, many=False, context={'request': request})
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    # def patch(self, request):
    #     data = request.data
    #     user = request.user
    #     serializer = UserSerializer(user, data, partial=True)
    #     # password = data.get('password')
    #     # if user.check_password(password):
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(
    #             serializer.data,
    #             status=status.HTTP_200_OK
    #         )
    #
    #     return Response(
    #         serializer.errors,
    #         status=status.HTTP_400_BAD_REQUEST
    #     )


class EHubReportApiView(APIView):

    def post(self, request):
        data = request.data
        hub = data.get('hub')
        number_of_sells_product = data.get('number_of_sells_product')
        total_amount_of_sells_product = data.get('total_amount_of_sells_product')
        hub_qs = EHubInfo.objects.filter(id=hub)
        if hub_qs.exists():
            hub_report_qs = EHubReport.objects.filter(hub=hub)
            if not hub_report_qs.exists():
                EHubReport.objects.create(hub=hub_qs.first(), Date=localtime(now()).date(),
                                          number_of_sells_product=number_of_sells_product,
                                          total_amount_of_sells_product=total_amount_of_sells_product)
                return Response({"message": "E-hub report created successfully"})
            else:
                qs = hub_report_qs.first()
                if qs.Date.month == localtime(now()).month:
                    qs.number_of_sells_product = int(qs.number_of_sells_product) + int(number_of_sells_product)
                    qs.total_amount_of_sells_product = float(qs.total_amount_of_sells_product) + float(
                        total_amount_of_sells_product)
                    qs.save()
                    return Response({"message": "E-hub report update successfully"})
                else:
                    EHubReport.objects.create(hub=hub_qs.first(), Date=localtime(now()).date(),
                                              number_of_sells_product=number_of_sells_product,
                                              total_amount_of_sells_product=total_amount_of_sells_product)
                    return Response({"message": "E-hub report created successfully"})
        else:
            return Response({"message": "E-hub not found"}, status=status.HTTP_404_NOT_FOUND)


class EditProfileApiView(APIView):
    def patch(self, request):
        user_id = request.data.get('user_id')
        print(user_id)
        profile_pic = request.data.get('profile_pic')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        email = request.data.get('email')
        phone_number = request.data.get('phone_number')
        is_email_own = User.objects.filter(email=email, id=user_id).first()
        is_email = User.objects.filter(email=email).exclude(email=is_email_own)
        if is_email.exists():
            return Response({"message": "Email already taken"}, status=status.HTTP_400_BAD_REQUEST)
        # if is_email.exists():
        user_qs = User.objects.filter(id=user_id)
        if user_qs.exists():
            user_qs = user_qs.first()
            user_qs.first_name = first_name
            user_qs.last_name = last_name
            user_qs.email = email
            user_qs.phone_number = phone_number

            if profile_pic:
                print('aaaaaa', profile_pic)
                user_details_qs = UserDetails.objects.filter(user=user_qs).first()
                user_details_qs.profile_pic = profile_pic
                user_details_qs.save()
            user_qs.save()
            return Response({"message": "User Details Successfully changed"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "User not found"}, status=status.HTTP_400_BAD_REQUEST)


class UserResetPasswordApiView(APIView):
    permission_classes = [AllowAny, ]
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            # user = get_object_or_404(User, email=data['email'])
            user = User.objects.filter(
                Q(email=data['identifier']) | Q(phone_number=data['identifier']))
            if user.exists():
                user = user.first()
                expire_time = timezone.now() + timedelta(hours=48)

                new_uuid = ResetPassword.objects.create(**{
                    'user_id': user.id,
                    'expire_time': expire_time
                })
                uid = unique_uuid_generator(instance=new_uuid)
                new_uuid.uuid = uid
                new_uuid.save()

                ResetPassword.objects.filter(user_id=user.id, active=True).exclude(id=new_uuid.id).update(active=False)
                try:
                    frontend_url = settings.FRONT_END_URL + "/reset-password/?code={}".format(new_uuid.uuid)
                    html_template = render_to_string('email/password-reset.html', context={'link': frontend_url,
                                                                                           'code': new_uuid.uuid})
                    send_html_mail(subject='Reset Password', html_content=html_template, recipient_list=[user.email])
                    return Response({
                        'message': 'Email send successfully'
                    }, status=status.HTTP_200_OK)
                except Exception as e:
                    return Response({'message': 'Unable to send email'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    "message": "User not found"
                }, status=status.HTTP_403_FORBIDDEN)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserResetPasswordConfirmApiView(APIView):
    permission_classes = [AllowAny, ]
    serializer_class = ResetPasswordConfirmSerializer

    def post(self, request):
        uuid = request.data.get('code')
        print(uuid)
        reset_object = get_object_or_404(ResetPassword, uuid=uuid, active=True)
        serializer = self.serializer_class(data=request.data)
        utc = pytz.UTC

        if reset_object.expire_time.replace(tzinfo=utc) < timezone.now().replace(tzinfo=utc):
            return Response({"message": "Code has expired."}, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            reset_object.user.set_password(serializer.data.get('password'))
            reset_object.active = False
            reset_object.user.save()
            reset_object.save()
            return Response({"message": "Password Changed successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Password reset was not successful."}, status=status.HTTP_400_BAD_REQUEST)


class AddEHubPurchasePersonApiView(APIView):

    def post(self, request):
        data = request.data
        hub_id = data.get('hub_id')
        order_amount = data.get('order_amount')
        number_of_product = data.get('number_of_product')
        person_name = data.get('person_name')
        person_email = data.get('person_email')
        invoice_file = data.get('invoice_file')
        person_id = data.get('person_id')

        hub_qs = EHubInfo.objects.filter(pk=hub_id)
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


class EHubPersonApiView(APIView):

    def get(self, request):
        hub_id = request.query_params.get('hub')
        filter_op = request.query_params.get('filter_op', '')
        print(filter_op)
        hub_qs = EHubInfo.objects.filter(pk=hub_id)
        # hub_qs = EHubInfo.objects.filter(user=request.user)
        print(hub_qs)
        if hub_qs.exists():
            hub_qs = hub_qs.first()
            if filter_op == "seven":
                hub_person_qs = EHubPurchasePerson.objects.filter(hub=hub_qs,
                                                                  Date__gte=timezone.now() - timedelta(days=7))
                print(hub_person_qs)
            elif filter_op == "month":
                hub_person_qs = EHubPurchasePerson.objects.filter(hub=hub_qs,
                                                                  Date__gte=timezone.now() - timedelta(days=30))
            elif filter_op == "year":
                hub_person_qs = EHubPurchasePerson.objects.filter(hub=hub_qs,
                                                                  Date__gte=timezone.now() - timedelta(days=365))
            else:
                hub_person_qs = EHubPurchasePerson.objects.filter(hub=hub_qs)
            serializer = EHubPersonSerializer(hub_person_qs, many=True)
            return Response(serializer.data)

        else:
            return Response({"message": "EHub Not Found"})

        # hub_id = EHubPurchasePerson.objects.filter(hub)


class TotalEHubPurchaseApiView(APIView):

    def get(self, request):
        hub_id = request.query_params.get('hub')
        hub_qs = EHubInfo.objects.filter(pk=hub_id)
        if hub_qs.exists():
            hub_qs = hub_qs.first()
            total = EHubPurchasePerson.objects.filter(hub=hub_qs).aggregate(total=Sum('total_amount_of_sells_product'))
        else:
            return Response({"message": "EHub Not Found"})
        return Response({"message": total})


class EHubViewSets(viewsets.GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = EHubInfo.objects.all()
    serializer_class = EHubShortSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = EHubDetailsSerializer(instance)
        return Response(serializer.data)
