from rest_framework import serializers
from account.models import CustomUserModel
from ..models import TransactionModel
from rest_framework.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status, generics
from rest_framework.response import Response
from django.utils import timezone

class StartTransferSerializer(serializers.Serializer):
    def create(self, validated_data):
        request = self.context['request']
        sender = request.user  
        
        transaction = TransactionModel.objects.create(
            sender=sender,
            status="pending",
            transaction_type="transfer",
            amount=0
        )
        
        # Store transaction_id in session
        request.session['transaction_id'] = transaction.id
        self.context['transaction'] = transaction
        return transaction 

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

        transaction_id = request.session.get('transaction_id')
        transaction = get_object_or_404(TransactionModel, id=transaction_id, sender=sender)

        transaction.receiver = recipient
        print("transer recipient", recipient)
        transaction.current_stage=1
        transaction.save()


        # Pass recipient and transaction to context
        self.context['recipient'] = recipient
        self.context['transaction'] = transaction

        return attrs 
    
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
    
    def validate_amount(self, amount):
        request = self.context['request']
        user = request.user 
        # Retrieve transaction from session
        transaction_id = request.session.get('transaction_id')
        transaction = get_object_or_404(TransactionModel, id=transaction_id, sender=user)

        # Ensure we are at stage 1
        if transaction.current_stage != 1:
            return Response({'error': 'Invalid transaction stage'}, status=status.HTTP_400_BAD_REQUEST)

        if amount < 0:
            raise serializers.ValidationError("The requested amount can not be less than zero")
        
        if amount > user.balance:
            raise serializers.ValidationError("The requested amount is more than your balance.")
        
        # Update transaction
        transaction.amount = amount
        transaction.current_stage = 2 
        transaction.save()

        # Store amount in session
        request.session['amount'] = str(amount)

        return amount
    
class ConfirmTransferSerializer(serializers.Serializer):

    def save(self):

        request = self.context['request']
        # recipient=self.context['recipient']
        amount=self.context['amount']

        user = request.user

        
        transaction_id = request.session.get('transaction_id')
        current_transaction = get_object_or_404(TransactionModel, id=transaction_id, sender=user)
        
        if current_transaction.current_stage != 2:
            raise serializers.ValidationError("Invalid transaction stage")
        
        recipient=current_transaction.receiver
            
        with transaction.atomic():
            # Update balances
            user.balance -= amount
            recipient.balance += amount

            user.save()
            recipient.save()

            current_transaction.status = "completed"  # Mark as completed after the transfer
            current_transaction.current_stage = 3  # Mark stage as 3 (confirmation stage)
            current_transaction.completed_at=timezone.now()
            current_transaction.save()
        

        # Return response data with updated balances and transaction details
        return {
            "sender_balance": user.balance,
            "recipient_balance": recipient.balance,
            "transaction_type": "transfer",
            "transaction_status": "completed",
            "transaction_stage": 3,

        }
