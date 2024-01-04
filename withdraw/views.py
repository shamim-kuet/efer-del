from rest_framework import viewsets, views, response, permissions, status
from .models import BankAccount, Withdraw
from wallet.models import Wallet
from .serializers import BankAccountSerializer, WithdrawSerializer
from django.db.models import Sum


class BankAccountViewSets(viewsets.ModelViewSet):
    serializer_class = BankAccountSerializer
    queryset = BankAccount.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return response.Response(serializer.data)
        else:
            return response.Response(serializer.errors)


    def list(self, request, *args, **kwargs):
        queryset = self.queryset.filter(user=request.user)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)



class WithdrawApiView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        data = request.data
        balance = data.get('withdraw_balance')
        # wallet = data.get('wallet')
        # wallet_qs = Wallet.objects.filter(id=wallet).first()
        wallet_qs = Wallet.objects.filter(user=request.user).first()
        if float(wallet_qs.minimum_withdraw) <=  float(wallet_qs.balance) >= float(balance):
            if float(balance) >= float(wallet_qs.minimum_withdraw):
                serializer = WithdrawSerializer(data=data)
                if serializer.is_valid():
                    serializer.save(user=request.user, wallet=wallet_qs)
                    wallet_qs.balance = float(wallet_qs.balance) - float(balance)
                    wallet_qs.save()
                    return response.Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return response.Response(serializer.errors)
            else:
                return response.Response({
                    "message": f"Minium withdraw amount is {wallet_qs.minimum_withdraw} pounds"
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return response.Response({
                "message": "You don't have sufficient balance to withdraw"
            }, status=status.HTTP_400_BAD_REQUEST)


class WithdrawUserReportApiView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        qs = Withdraw.objects.filter(user=user)
        calculate = qs.aggregate(sum=Sum('withdraw_balance'))
        serializer = WithdrawSerializer(qs, many=True)
        if qs.exists():
            last_withdraw = qs.first().withdraw_balance
            return response.Response({"total_withdraw": calculate, "last_withdraw": last_withdraw, "data": serializer.data})
        else:
            return response.Response({"total_withdraw": calculate, "last_withdraw": 0, "data": serializer.data})


class DeleteWithdrawApiView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        user = request.user
        qs = Withdraw.objects.filter(user=user, pk=pk)
        if qs.exists():
            qs = qs.first()
            qs.delete()
            return response.Response({"data": "Deleted Successfully"}, status=status.HTTP_202_ACCEPTED)
        else:
            return response.Response({"data": "Account not found"}, status=status.HTTP_400_BAD_REQUEST)



