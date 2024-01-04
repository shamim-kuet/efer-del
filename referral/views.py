from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from django.utils.timezone import localtime, now
from rest_framework.response import Response
from .models import Referral, ReferredPerson, ReferralReport
from user.models import EHubInfo, EHubReport, EHubPurchasePerson
from .serializers import ReferralReportSerializer, ReferredPersonSerializer, ReferralSerializer
from wallet.models import Wallet
from efranchise.utils import send_html_mail
from django.template.loader import render_to_string
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.db.models.functions import ExtractYear, ExtractMonth, ExtractDay
from django.db.models import Sum, F, When, Case, Value, CharField


class AddReferralApiView(APIView):
    def post(self, request):
        data = request.data
        code = data.get('code')
        referred_person_name = data.get('referred_person_name')
        referred_person_id = data.get('referred_person_id')
        referred_person_email = data.get('referred_person_email')
        referred_person_country = data.get('referred_person_country')
        referrer = Referral.objects.filter(referral_code=code)
        if referrer.exists():
            referrer = referrer.first()
            referred = ReferredPerson.objects.filter(referred_person_email=referred_person_email)
            if referred.exists():
                # if hub_id:
                #     hub_qs = EHubInfo.objects.filter(pk=hub_id).first()
                #     hub_report_qs = EHubReport.objects.filter(hub=hub_qs)
                #     if hub_report_qs.exists():
                #         hub_report_qs = hub_report_qs.first()
                #         if hub_report_qs.Date.month == localtime(now()).month:
                #             hub_report_qs.number_of_sells_product += 1
                #             hub_report_qs.total_amount_of_sells_product +=
                return Response({"message": "Referrer Already Registered"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                ReferredPerson.objects.create(
                    referral=referrer, referred_person_name=referred_person_name, referred_person_id=referred_person_id,
                    referred_person_email=referred_person_email, referred_person_country=referred_person_country
                )
                referrer.total_referral = referrer.total_referral + 1
                referrer.save()
                return Response({"message": "Referral Successfully registered"}, status=status.HTTP_201_CREATED)

        else:
            return Response({"message": "Referrer Not Found"}, status=status.HTTP_400_BAD_REQUEST)


# class AddEHubPurchasePerson(APIView):
#
#     def post(self, request):
#         hub_id = data.get('hub_id')
#         referred_person_order_amount = data.get('referred_person_order_amount')
#         number_of_product = data.get('number_of_product')
#         person_name = data.get('person_name')
#         person_email = data.get('person_email')
#         invoice_file = data.get('invoice_file')
#
#         if hub_id:
#             hub_qs = EHubInfo.objects.filter(pk=hub_id)
#             if hub_qs.exists():
#                 hub_qs = hub_qs.first()
#                 EHubPurchasePerson.objects.create(hub=hub_qs, person_name=person_name, person_email=person_email,
#                                                   person_id=referred_person_id,
#                                                   number_of_sells_product=number_of_product,
#                                                   total_amount_of_sells_product=referred_person_order_amount,
#                                                   invoice=invoice_file)
#                 return Response({"message": "EHub Person Added Successfully"})
#         return Response({"message": "EHub Not Found"})


class AddReferralOrderApiView(APIView):
    def post(self, request):
        data = request.data
        print(data)
        code = data.get('code')
        referred_person_order_amount = data.get('referred_person_order_amount')
        # referred_person_id = data.get('referred_person_id')
        referred_person_email = data.get('referred_person_email')
        # hub_id = data.get('hub_id')
        # number_of_product = data.get('number_of_product')
        # person_name = data.get('person_name')
        # person_email = data.get('person_email')
        # invoice_file = data.get('invoice_file')

        # if hub_id:
        #
        #     hub_qs = EHubInfo.objects.filter(pk=hub_id)
        #     if hub_qs.exists():
        #         hub_qs = hub_qs.first()
                # EHubPurchasePerson.objects.create(hub=hub_qs, person_name=person_name, person_email=person_email,
                #                                   person_id=referred_person_id,
                #                                   number_of_sells_product=number_of_product,
                #                                   total_amount_of_sells_product=referred_person_order_amount,
                #                                   invoice=invoice_file)
                # hub_report_qs = EHubReport.objects.filter(hub=hub_qs)
                # if hub_report_qs.exists():
                #     hub_report_qs = hub_report_qs.first()
                #     if hub_report_qs.Date.month == localtime(now()).month:
                #         hub_report_qs.number_of_sells_product = int(hub_report_qs.number_of_sells_product) + \
                #                                                 int(number_of_product)
                #         hub_report_qs.total_amount_of_sells_product = \
                #             float(hub_report_qs.total_amount_of_sells_product) \
                #             + float(referred_person_order_amount)
                #
                #         hub_report_qs.save()
                #     else:
                #         EHubReport.objects.create(hub=hub_qs, Date=localtime(now()).date(),
                #                                   number_of_sells_product=number_of_product,
                #                                   total_amount_of_sells_product=referred_person_order_amount)
                # else:
                #     EHubReport.objects.create(hub=hub_qs, Date=localtime(now()).date(),
                #                               number_of_sells_product=number_of_product,
                #                               total_amount_of_sells_product=referred_person_order_amount)

        # qs = ReferredPerson.objects.filter(referral__referral_code=code, referred_person_id=referred_person_id)
        qs = ReferredPerson.objects.filter(referral__referral_code=code, referred_person_email=referred_person_email)
        if qs.exists():
            referrer = Referral.objects.filter(referral_code=code).first()
            qs = qs.first()

            # if referrer.purchase_limit_per_user <= qs.total_purchase_time:
            #     qs.referred_person_last_order_amount = referred_person_order_amount
            #     qs.total_purchase_amount = float(qs.total_purchase_amount) + float(referred_person_order_amount)
            #     qs.save()
            #     return Response({"message": "Referral has already exceed it's limit"},
            #                     status=status.HTTP_400_BAD_REQUEST)
            # else:
            qs.referred_person_last_order_amount = referred_person_order_amount
            if float(referred_person_order_amount) >= float(referrer.minimum_purchase_per_user):
                if qs.total_purchase_time == 0:
                    referrer.number_of_referral_confirmed_purchase = \
                        referrer.number_of_referral_confirmed_purchase + 1
                    if referrer.number_of_referral_confirmed_purchase % referrer.purchase_limit_per_user == 0 and \
                            referrer.number_of_referral_confirmed_purchase > 0:
                        referrer.total_referral_income += 10
                        wallet_qs = Wallet.objects.filter(user=referrer.user).first()
                        print(wallet_qs)
                        wallet_qs.balance += 10
                        wallet_qs.save()
                        report_qs = ReferralReport.objects.filter(user=referrer.user)
                        if not report_qs.exists():
                            ReferralReport.objects.create(user=referrer.user, Date=localtime(now()).date(),
                                                          profit=referrer.referral_discount)
                        else:
                            report_qs = report_qs.last()
                            if report_qs.Date.month == localtime(now()).month:
                                report_qs.profit += referrer.referral_discount
                                report_qs.save()
                            else:
                                ReferralReport.objects.create(user=referrer.user, Date=localtime(now()).date(),
                                                              profit=referrer.referral_discount)
                            # if qs.Date.month < localtime(now()).date():
                            #     ReferralReport.objects.create(user=referrer.user, Date=localtime(now()).date())
                            # else:

                    qs.total_purchase_time = qs.total_purchase_time + 1

                referrer.save()

            qs.total_purchase_amount = float(qs.total_purchase_amount) + float(referred_person_order_amount)
            qs.save()

            return Response({"message": "Referral discount added successfully"},
                            status=status.HTTP_200_OK)

        else:
            return Response({"message": "Referral Not Found"}, status=status.HTTP_400_BAD_REQUEST)


class ReferralPersonInfoUpdateApiView(APIView):
    def post(self, request):
        data = request.data
        code = data.get('code')
        referred_person_email = data.get('referred_person_email')
        referred_person_name = data.get('referred_person_name')
        qs = ReferredPerson.objects.filter(referral__referral_code=code, referred_person_email=referred_person_email)
        if qs.exists():
            qs = qs.first()
            qs.referred_person_name = referred_person_name
            qs.save()
            return Response({"message": "Profile successfully updated"})
        return Response({"message": "Referral user not found"})


class UserReferral(APIView):
    def get(self, request):
        # referred_person_qs = ReferredPerson.objects.filter(referral__user=request.user)
        referral_qs = Referral.objects.filter(user=request.user).first()
        serializer = ReferralSerializer(referral_qs, many=False)
        return Response(serializer.data)


class MonthlyReferralApiView(APIView):

    def get(self, request):
        # referral_person_qs = ReferredPerson.objects.filter(referral__user=request.user).annotate(month=TruncMonth('updated_at').annotate(total_amount=Sum('balance')))
        referral_person_qs = ReferralReport.objects.filter(user=request.user)
        # total_qs = referral_person_qs.annotate(year=ExtractYear('Date')).values('year').annotate(profit=Sum(F('profit') + F('company_profit'))).values('year', 'profit')
        # total_day_qs = referral_person_qs.annotate(day=ExtractDay('Date')).values('day').annotate(profit=Sum(F('profit') + F('company_profit'))).values('day', 'profit')
        # print(total_day_qs)
        # total_qs_m = referral_person_qs.annotate(month=ExtractMonth('Date')).annotate(month=Case(
        #     When(month=1, then=Value("Jan")),
        #     When(month=2, then=Value("Feb")),
        #     When(month=3, then=Value("Mar")),
        #     When(month=4, then=Value("Apr")),
        #     When(month=5, then=Value("May")),
        #     When(month=6, then=Value("Jun")),
        #     When(month=7, then=Value("July")),
        #     When(month=8, then=Value("Aug")),
        #     When(month=9, then=Value("Sept")),
        #     When(month=10, then=Value("Oct")),
        #     When(month=11, then=Value("Nov")),
        #     When(month=12, then=Value("Dec")),
        #     output_field=CharField()
        # )).values('month').annotate(profit=Sum(F('profit') + F('company_profit'))).values('month', 'profit')
        # print(total_qs_m)
        # print(referral_person_qs.annotate(year=ExtractYear('Date')).values('month').annotate(profit=Sum(F('profit') + F('company_profit'))).values('month', 'profit'))
        serializer = ReferralReportSerializer(referral_person_qs, many=True)
        return Response(serializer.data)


class YearlyReferralApiView(APIView):

    def get(self, request):
        referral_person_qs = ReferralReport.objects.filter(user=request.user)
        total_qs = referral_person_qs.annotate(year=ExtractYear('Date')).values('year').annotate(
            profit=Sum(F('profit') + F('company_profit'))).values('year', 'profit')

        referral_total_qs = referral_person_qs.annotate(year=ExtractYear('Date')).values('year')\
            .annotate(profit=Sum('profit')).values('year', 'profit')

        return Response({
            "total_qs": total_qs,
            "referral_total_qs": referral_total_qs
        })


class UserReferralPerson(APIView):
    def get(self, request):
        referred_person_qs = ReferredPerson.objects.filter(referral__user=request.user)
        # referral_qs = Referral.objects.filter(user=request.user).first()
        # per_page = 6
        # page = int(request.query_params.get('page', 1))
        # start = (page - 1) * per_page
        # end = page * per_page
        # total = len(referred_person_qs)
        # data =ReferredPersonSerializer(referred_person_qs[start:end], many=True).data
        # return Response({
        #     'data': data,
        #     'meta': {
        #         'total': total,
        #         'page': page,
        #         'last_page': math.ceil(total / per_page)
        #     }
        # })
        serializer = ReferredPersonSerializer(referred_person_qs, many=True)
        return Response(serializer.data)


class ReminderEmailApiView(APIView):

    def get(self, request):
        referred = request.query_params.get('referrar')
        referred_qs = ReferredPerson.objects.filter(pk=referred).first()
        html_template = render_to_string('referral/reminder.html')
        if referred_qs.referred_person_email:
            try:
                send_html_mail(subject='Active Account', html_content=html_template,
                               recipient_list=[referred_qs.referred_person_email])
                return Response({
                    'message': 'Email send successfully',
                }, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'message': 'Unable to send email'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Email not found'}, status=status.HTTP_200_OK)


class DownloadReferralBannerApiView(APIView):

    def get(self, request):
        referral_id = int(request.query_params.get('referral_id'))
        referral_qs = Referral.objects.filter(id=referral_id).first()
        print(referral_qs.referral_code)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Report.pdf"'
        html_template = render_to_string('referral/referral-banner.html', context={"referral": referral_qs})
        pisaStatus = pisa.CreatePDF(html_template, dest=response)

        # return render(request, 'referral/referral-banner.html', context={"referral": referral_qs})
        return response
