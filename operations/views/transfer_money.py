from ..serializers import CheckAccountSerializer, CheckBalanceSerializer, ConfirmTransferSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from account.models import CustomUserModel
from decimal import Decimal
from ..permissions import IsGoldUserPermission
from ..models import TransactionModel
from django.shortcuts import get_object_or_404

class CheckAccountView(APIView):
    permission_classes = [IsGoldUserPermission]
    def post(self, request):
        serializer=CheckAccountSerializer(data=request.data, context={"request": request})
        
        if serializer.is_valid():
            # Get the recipient and transaction from the serializer context
            recipient = serializer.context['recipient']
            transaction = serializer.context['transaction']

            return Response(
                {
                    "message": "Requested account is valid",
                    "transaction_id": transaction.transaction_id,
                    "recipient_phone_number": recipient.phone_number,
                }, 
                status=status.HTTP_200_OK
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckBalanceView(APIView):
        permission_classes = [IsGoldUserPermission]
        def post(self, request):

            serializer=CheckBalanceSerializer(data=request.data, context={'request': request})
            transaction_id = request.data.get("transaction_id")  # Receive transaction_id dynamically

            if not transaction_id:
                return Response({"error": "Transaction ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        
            if serializer.is_valid():
                return Response(
                                {
                                 "message": "Requested amount is valid",
                                 "transaction_id": transaction_id,
                                 },
                                   status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class ConfirmTransferView(APIView):
    permission_classes = [IsGoldUserPermission]
    def post(self, request):

        transaction_id = request.data.get("transaction_id")  # Receive transaction_id dynamically

        if not transaction_id:
            return Response({"error": "Transaction ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        transfer_serializer = ConfirmTransferSerializer(
            data=request.data,
            context={
                'request': request,
            }
        )
        
        if transfer_serializer.is_valid():
            response_data = transfer_serializer.save()

            return Response({
                "message": "Transfer successful",
                "sender_balance": response_data["sender_balance"],
                "recipient_balance": response_data["recipient_balance"],
                "transaction_type": response_data["transaction_type"],
                "transaction_status": response_data["transaction_status"],
                "transaction_stage": response_data["transaction_stage"]
            }, status=status.HTTP_200_OK)
            
        return Response(transfer_serializer.errors, status=400)



class CheckTransactionStatusView(APIView):
    permission_classes = [IsGoldUserPermission]

    def get(self, request, transaction_id):
        # Get the transaction by ID and ensure it's the user's transaction
        transaction = get_object_or_404(TransactionModel, transaction_id=transaction_id, sender=request.user)
        
        # Determine the stage of the transaction and return relevant data
        if transaction.current_stage == 0:
            # Stage 1: phone_number input required
            return Response({
                'status': 'pending',
                'stage': 1,
                'fields': ['phone_number'],
                'transaction_id': transaction.transaction_id
            })
        
        elif transaction.current_stage == 1:
            # Stage 2: amount input required
            return Response({
                'status': 'pending',
                'stage': 2,
                'fields': ['amount'],
                'transaction_id': transaction.transaction_id
            })
        elif transaction.current_stage == 2:
            # Stage 3: confirmation required
            return Response({
                'status': 'completed',
                'stage': 3,
                'transaction_id': transaction.transaction_id
            })
        else:
            # If the transaction is in an invalid state, return an error
            return Response({
                'error': 'Invalid transaction stage'
            }, status=status.HTTP_400_BAD_REQUEST)