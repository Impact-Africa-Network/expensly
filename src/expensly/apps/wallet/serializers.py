from .models import Transaction, Request
from rest_framework import serializers

class TransactionCreateSerializer(serializers.ModelSerializer):
    """Create a Transaction Serializer"""
    class Meta:
        model = Transaction
        fields = ["amount"]

class TransactionDetailSerializer(serializers.ModelSerializer):
    """Transaction Detail Serializer"""
    class Meta:
        model = Transaction
        fields = '__all__'

class RequestCreateSerializer(serializers.ModelSerializer):
    """
    Create a Request Serializer
    """

    class Meta:
        model = Request
        fields = ["amount", "purpose"]
