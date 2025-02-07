from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import TransferTransactionModel
from ..serializers import (
    AddAccountSerializer,
    AddAmountSerializer,
    ConfirmTransactionSerializer
)
from django.core.exceptions import ValidationError
from django.utils import timezone
from account.models import CustomUserModel
from django.db import transaction


class CheckStatusView(APIView):
    def get(self, request):
        transaction_id = request.GET.get("transaction_id")
        if not transaction_id:
            return Response({"error": "Transaction ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            transaction = TransferTransactionModel.objects.get(transaction_id=transaction_id)
        except TransferTransactionModel.DoesNotExist:
            return Response({"error": "Invalid Transaction ID"}, status=status.HTTP_404_NOT_FOUND)

        input_fields = []
        if transaction.status == "pending_account":
            input_fields = ["account_number"]
        elif transaction.status == "pending_amount":
            input_fields = ["amount"]
        elif transaction.status == "pending_confirmation":
            input_fields = ["confirm_button"]

        return Response({
            "transaction_id": str(transaction.transaction_id),
            "status": transaction.status,
            "input_fields": input_fields
        })


class AddAccountView(APIView):
    def post(self, request):
        serializer = AddAccountSerializer(data=request.data)
        if serializer.is_valid():
            sender = request.user 
            receiver = CustomUserModel.objects.get(phone_number=serializer.validated_data["receiver"])
            
            new_transaction = TransferTransactionModel.objects.create(
                sender=sender,
                receiver=receiver,
                status="pending_amount"
            )

            return Response({"transaction_id": new_transaction.transaction_id, "status": new_transaction.status}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddAmountView(APIView):
    def post(self, request):
        serializer = AddAmountSerializer(data=request.data)
        if serializer.is_valid():
            transaction_id = serializer.validated_data["transaction_id"]
            amount = serializer.validated_data["amount"]

            try:
                transaction = TransferTransactionModel.objects.get(transaction_id=transaction_id)
            except TransferTransactionModel.DoesNotExist:
                return Response({"error": "Invalid Transaction ID"}, status=status.HTTP_404_NOT_FOUND)

            if transaction.status != "pending_amount":
                return Response({"error": "Invalid step"}, status=status.HTTP_400_BAD_REQUEST)

            transaction.amount = amount
            transaction.status = "pending_confirmation"
            transaction.save()

            return Response({"message": "Amount added", "status": transaction.status})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfirmTransactionView(APIView):
    def post(self, request):
        serializer = ConfirmTransactionSerializer(data=request.data)
        if serializer.is_valid():
            transaction_id = serializer.validated_data["transaction_id"]

            try:
                new_transaction = TransferTransactionModel.objects.get(transaction_id=transaction_id)
            except TransferTransactionModel.DoesNotExist:
                return Response({"error": "Invalid Transaction ID"}, status=status.HTTP_404_NOT_FOUND)

            if new_transaction.status != "pending_confirmation":
                return Response({"error": "Invalid step"}, status=status.HTTP_400_BAD_REQUEST)
            
            sender = new_transaction.sender
            receiver = new_transaction.receiver
            amount = new_transaction.amount

            try:
                with transaction.atomic():
                    # Deduct from sender
                    sender.balance -= amount
                    sender.save()

                    # Add to receiver
                    receiver.balance += amount
                    receiver.save()

                    # Mark transaction as completed
                    new_transaction.status = 'completed'
                    new_transaction.completed_at = timezone.now()
                    new_transaction.save()

            except Exception as e:
                raise ValidationError(f"Transaction failed: {str(e)}")

            return Response({"message": "Transaction completed successfully", "status": new_transaction.status})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

