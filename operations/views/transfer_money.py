from ..serializers import CheckAccountSerializer, CheckBalanceSerializer, ConfirmTransferSerializer, StartTransferSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from account.models import CustomUserModel
from decimal import Decimal
from ..permissions import IsGoldUserPermission

class StartTransferView(APIView):
    permission_classes = [IsGoldUserPermission]
    def post(self, request):
        sender=request.user
        transfer_data = {
            'sender': sender,
        }
        serializer=StartTransferSerializer(data=transfer_data, context={"request":request})

        if serializer.is_valid():
            transaction = serializer.save()
            # transaction = serializer.context['transaction']

            return Response(
                {
                    "message": "You are allowed to transfer",
                    "transaction_id": transaction.id,
                    "sender_phone_number": sender.phone_number,
                }, 
                status=status.HTTP_200_OK
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
                    "validated_data": serializer.validated_data,
                    "transaction_id": transaction.id,
                    "recipient_phone_number": recipient.phone_number,
                }, 
                status=status.HTTP_200_OK
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckBalanceView(APIView):
        permission_classes = [IsGoldUserPermission]
        def post(self, request):
            serializer=CheckBalanceSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                return Response({"message": "Requested amount is valid"}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class ConfirmTransferView(APIView):
    permission_classes = [IsGoldUserPermission]
    def post(self, request):

        amount = request.session.get('amount')
        recipient = CustomUserModel.objects.get(id=request.session.get('recipient_id'))

        transfer_data = {
            'recipient': recipient,
            'amount': Decimal(amount)
        }

        transfer_serializer = ConfirmTransferSerializer(
            data=transfer_data,
            context={
                'request': request,
                'recipient': recipient,
                'amount':Decimal(amount)
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