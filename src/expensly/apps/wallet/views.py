from ian_auth import permissions
from . import models as ms
from rest_framework import viewsets
# from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from . import serializers as sz


# Create your views here.

class WalletModelViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AuthenticatedUser, ]
    serializer_class = sz.TransactionDetailSerializer
    queryset = ms.Transaction.objects.all()


    @action(
        methods=["POST"],
        detail=False,
        url_path='request-funds',
        permission_classes=[permissions.AuthenticatedUser]
    )
    def request_funds(self, request):

        serializer = sz.RequestCreateSerializer(data=data)

        if not serializer.is_valid():
            return Response({"error": True})

        data = serializer.validated_data
        funds_request = ms.Request.objects.create(amount=data.amount, purpose=data.purpose)
        funds_request.save()

        return Response({'success': True})

    # @action(
    #     methods=["POST"],
    #     detail=False,
    #     url_path='release-funds',
    #     permission_classes=[permissions.AuthenticatedUser]
    # )
    # def release_funds(self, request):

    #     serializer = sz.TransactionCreateSerializer(data=data)

    #     if not serializer.is_valid():
    #         return Response({"error": True})

    #     data = serializer.validated_data

    #     transaction = ms.Transaction.objects.create(amount=data.amount)
    #     transaction.save()

    #     return Response({'success': True})