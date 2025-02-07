from rest_framework import serializers
from ..models import TransferTransactionModel
from account.models import CustomUserModel

class AddAccountSerializer(serializers.Serializer):
    receiver = serializers.CharField(max_length=20)

    def validate_receiver(self, value):
        """Normalize and validate phone number."""
        value = value.strip().replace(" ", "")
        if value.startswith("0"):
            value = "+994" + value[1:]
        elif value.startswith("5"):
            value = "+994" + value
        elif not value.startswith("+994"):
            raise serializers.ValidationError("Invalid phone number format.")
        
        # Check if receiver exists in CustomUserModel
        if not CustomUserModel.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("Receiver account does not exist.")
        
        return value

class AddAmountSerializer(serializers.Serializer):
    transaction_id = serializers.UUIDField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    def validate(self, data):
        """Ensure amount is positive and does not exceed sender’s balance."""
        transaction_id = data.get("transaction_id")
        amount = data.get("amount")

        try:
            transaction = TransferTransactionModel.objects.get(transaction_id=transaction_id)
        except TransferTransactionModel.DoesNotExist:
            raise serializers.ValidationError("Invalid Transaction ID")

        if amount <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        
        if transaction.sender.balance < amount:
            raise serializers.ValidationError("Insufficient balance.")

        return data

class ConfirmTransactionSerializer(serializers.Serializer):
    transaction_id = serializers.UUIDField()
