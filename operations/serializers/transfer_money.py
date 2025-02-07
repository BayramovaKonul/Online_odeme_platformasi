from rest_framework import serializers
from account.models import CustomUserModel
from ..models import TransactionModel
from rest_framework.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status, generics
from rest_framework.response import Response
from django.utils import timezone

class CheckAccountSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    
    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        
        # Normalize the phone number
        normalized_phone = self.normalize_phone_number(phone_number)
        
        if not normalized_phone:
            raise ValidationError("Invalid phone number format. Use +994XXXXXXXXX, 05XXXXXXXX, or 5XXXXXXXX.")

        try:
            recipient = CustomUserModel.objects.get(phone_number=normalized_phone)
        except CustomUserModel.DoesNotExist:
            raise ValidationError("No account found with this phone number.")

        request = self.context['request']
        sender = request.user  # Get the authenticated user

        transaction = TransactionModel.objects.create(
            sender=sender,
            receiver=recipient,
            status="pending",
            transaction_type="transfer",
            current_stage=1,
            amount=0
        )

        # Store in context for use in the view
        self.context['recipient'] = recipient
        self.context['transaction'] = transaction

        return {
            "phone_number": phone_number,
            "transaction_id": transaction.transaction_id
        }
    
    def normalize_phone_number(self, value):
        """Normalize phone number to +994XXXXXXXXX format."""
        value = value.strip().replace(" ", "")  
        
        if value.startswith("0"): 
            return "+994" + value[1:]  
        elif value.startswith("5"): 
            return "+994" + value  
        elif value.startswith("+994"): 
            return value
        return None 
    
class CheckBalanceSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = serializers.UUIDField()

    def validate(self, attrs):
        request = self.context['request']
        user = request.user 

        transaction_id = attrs.get('transaction_id')
        print(transaction_id)
        transaction = get_object_or_404(TransactionModel, transaction_id=transaction_id, sender=user)
        print(transaction)

        # Ensure we are at stage 1
        if transaction.current_stage != 1:
            return Response({'error': 'Invalid transaction stage'}, status=status.HTTP_400_BAD_REQUEST)
        
        amount = attrs.get('amount')

        if amount < 0:
            raise serializers.ValidationError("The requested amount can not be less than zero")
        
        if amount > user.balance:
            raise serializers.ValidationError("The requested amount is more than your balance.")
        
        # Update transaction
        transaction.amount = amount
        transaction.current_stage = 2 
        transaction.save()


        attrs["transaction"] = transaction
        attrs["amount"] = amount
        self.context['transaction'] = transaction

        return attrs
    
class ConfirmTransferSerializer(serializers.Serializer):
    transaction_id = serializers.UUIDField()

    def validate(self, attrs):
        request = self.context['request']
        user = request.user

        transaction_id = attrs.get('transaction_id')
        current_transaction = get_object_or_404(TransactionModel, transaction_id=transaction_id, sender=user)
        
        if current_transaction.current_stage != 2:
            raise serializers.ValidationError("Invalid transaction stage")
        
        attrs['transaction'] = current_transaction
        return attrs

    def save(self, **kwargs):
        request = self.context['request']
        user = request.user
        current_transaction = self.validated_data['transaction']
        
        recipient = current_transaction.receiver
        amount = current_transaction.amount

        with transaction.atomic():
            # Update balances
            user.balance -= amount
            recipient.balance += amount

            user.save()
            recipient.save()

            current_transaction.status = "completed"  # Mark as completed after the transfer
            current_transaction.current_stage = 3  # Mark stage as 3 (confirmation stage)
            current_transaction.completed_at = timezone.now()
            current_transaction.save()
        
        # Return response data with updated balances and transaction details
        return {
            "transaction_id": str(current_transaction.transaction_id),
            "sender_balance": user.balance,
            "recipient_balance": recipient.balance,
            "transaction_type": "transfer",
            "transaction_status": "completed",
            "transaction_stage": 3,
        }
