from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Wallet
from referral.models import Referral
from .serializers import WalletSerializer
from django.db.models.functions import TruncMonth, TruncYear
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


class WalletApiView(APIView):

    def get(self, request):
        qs = Wallet.objects.filter(user=request.user).first()
        serializer = WalletSerializer(qs)
        return Response(serializer.data)


class WalletIndex(LoginRequiredMixin, View):
    template_name = "wallet/index.html"
    login_url = '/admin/login/'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"success": False, "message": ""})

    def post(self, request):
        print(request.POST.get('amount'))
        if request.POST.get('amount'):
            Referral.objects.all().update(referral_discount=request.POST.get('amount'))
            return render(request, self.template_name, {"success": True,
                                                        "message": "Referral discount has been updated"})
        elif request.POST.get('user_number'):
            Referral.objects.all().update(purchase_limit_per_user=request.POST.get('user_number'))
            return render(request, self.template_name, {"success": True,
                                                        "message": "Number of users have been updated"})

        elif request.POST.get('minimum_purchase'):
            Referral.objects.all().update(minimum_purchase_per_user=request.POST.get('minimum_purchase'))
            return render(request, self.template_name, {"success": True,
                                                        "message": "Minimum purchase of a user has been updated"})

        return render(request, self.template_name, {"success": True, "message": ""})

# class DeclareCompanyProfit(APIView):
#     def post(self, request):
#         user_id =
