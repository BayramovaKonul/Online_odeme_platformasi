from rest_framework import generics
from ..models import PaymentTypesModel, ProjectsModel, PaymentTransactionModel
from ..serializers import AddPaymentInputSerializer, AddPaymentAmountSerializer, ConfirmPaymentSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.utils import timezone

# class ChoosePaymentTypeView(APIView):

#     def post(self, request, payment_type_id):
#         sender=request.user
       
#         serializer = ChoosePaymentTypeSerializer(
#             data=request.data,
#             context={"request": request, "payment_type_id": payment_type_id}
#         )

#         if serializer.is_valid():
#             transaction = serializer.save()

#             return Response(
#                 {
#                     "message": "Payment Type was chosen",
#                     "transaction_id": transaction.transaction_id,
#                     "payment_type": PaymentTypesModel.objects.get(id=payment_type_id).name
#                 },
#                 status=status.HTTP_200_OK
#             )

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# class ChooseProjectView(APIView):

#     def post(self, request, project_id):
       
#         serializer = ChooseProjectSerializer(
#             data=request.data,
#             context={"request": request, 
#                      "project_id": project_id}
#         )

#         if serializer.is_valid():
             
#             transaction = serializer.validated_data.get("transaction")  
#             if not transaction:
#                 return Response({"error": "Transaction was not processed correctly."}, status=status.HTTP_400_BAD_REQUEST)

#             return Response(
#                 {
#                     "message": "Project was chosen",
#                     "transaction_id": transaction.transaction_id,
#                     "project": ProjectsModel.objects.get(id=project_id).name
#                 },
#                 status=status.HTTP_200_OK
#             )

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# class CheckPaymentValueView(APIView):

#     def post(self, request):
       
#         serializer = CheckPaymentValueSerializer(
#             data=request.data,
#             context={"request": request}
#         )

#         if serializer.is_valid():
             
#             transaction = serializer.validated_data.get("transaction")  # Use validated_data
#             if not transaction:
#                 return Response({"error": "Transaction was not processed correctly."}, status=status.HTTP_400_BAD_REQUEST)

#             return Response(
#                 {
#                     "message": "Requested account is valid",
#                     "transaction_id": transaction.transaction_id,
#                     "value": transaction.value,
#                 },
#                 status=status.HTTP_200_OK
#             )

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class CheckPaymentAmountView(APIView):

#     def post(self, request):
       
#         serializer = CheckPaymentAmountSerializer(
#             data=request.data,
#             context={"request": request}
#         )

#         if serializer.is_valid():
             
#             transaction = serializer.context.get('transaction')
#             if not transaction:
#                 return Response({"error": "Transaction was not processed correctly."}, status=status.HTTP_400_BAD_REQUEST)

#             return Response(
#                 {
#                     "message": "Requested account is valid",
#                     "transaction_id": transaction.transaction_id,
#                     "amount": transaction.amount,
#                 },
#                 status=status.HTTP_200_OK
#             )

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# class ConfirmPaymentView(APIView):
#     def post(self, request):

#         serializer = ConfirmPaymentSerializer(
#             data=request.data,
#             context={
#                 'request': request,
#             }
#         )
        
#         if serializer.is_valid():
#             response_data = serializer.save()

#             return Response({
#                 "message": "Payment successful",
#                 "balance_after_payment": response_data["balance_after_payment"],
#                 "payment_type": response_data["payment_type"],
#                 "transaction_type": response_data["transaction_type"],
#                 "project": response_data["project"],
#                 "transaction_status": response_data["transaction_status"]
#             }, status=status.HTTP_200_OK)
            
#         return Response(serializer.errors, status=400)


class AddPaymentInputView(APIView):
    def post(self, request):
        serializer = AddPaymentInputSerializer(data=request.data)
        if serializer.is_valid():
            project = serializer.validated_data["project"]
            payment_data = serializer.validated_data["payment_data"]

            # Validate input fields based on project’s payment type
            required_fields = project.type.required_inputs

            # Ensure all required fields are provided
            for field_name, field_props in required_fields.items():
                if field_props.get("required", False) and field_name not in payment_data:
                    return Response({field_name: "This field is required."}, status=status.HTTP_400_BAD_REQUEST)

            # Create transaction
            transaction = PaymentTransactionModel.objects.create(
                project=project,
                payment_data=payment_data,
                current_stage=1,
                user=request.user,
            )

            return Response({"transaction_id": transaction.transaction_id, "status": transaction.status, "current_step":transaction.current_stage}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddPaymentAmountView(APIView):
    def post(self, request):
        print("Post method started")
        print("Request Data:", request.data)  
        
        serializer = AddPaymentAmountSerializer(data=request.data)

        if serializer.is_valid():
            transaction_id = serializer.validated_data["transaction_id"]
            amount = serializer.validated_data["amount"]

            print(transaction_id)
            transaction = PaymentTransactionModel.objects.get(transaction_id=transaction_id)

            try:
                transaction = PaymentTransactionModel.objects.get(transaction_id=transaction_id)
            except PaymentTransactionModel.DoesNotExist:
                return Response({"error": "Invalid Transaction ID"}, status=status.HTTP_404_NOT_FOUND)

            if transaction.current_stage != 1:
                return Response({"error": "Invalid step"}, status=status.HTTP_400_BAD_REQUEST)

            transaction.amount = amount
            transaction.current_stage = 2
            transaction.save()

            return Response({"message": "Amount added", "status": transaction.status})
        
        print(f"Serializer is NOT valid. Errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfirmPaymentView(APIView):
    def post(self, request):
        serializer = ConfirmPaymentSerializer(data=request.data)
        if serializer.is_valid():
            transaction_id = serializer.validated_data["transaction_id"]

            try:
                transaction = PaymentTransactionModel.objects.get(transaction_id=transaction_id)
            except PaymentTransactionModel.DoesNotExist:
                return Response({"error": "Invalid Transaction ID"}, status=status.HTTP_404_NOT_FOUND)

            if transaction.current_stage != 2:
                return Response({"error": "Invalid step"}, status=status.HTTP_400_BAD_REQUEST)

            # Finalizing transaction
            transaction.status = "completed"
            transaction.current_stage = 3
            transaction.completed_at = timezone.now()
            transaction.user.balance -= transaction.amount
            transaction.save()

            return Response({
                "message": "Payment confirmed successfully!",
                "status": transaction.status
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckPaymentStatusView(APIView):
    def get(self, request):
        transaction_id = request.GET.get("transaction_id")
        if not transaction_id:
            return Response({"error": "Transaction ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            transaction = PaymentTransactionModel.objects.get(transaction_id=transaction_id)
        except PaymentTransactionModel.DoesNotExist:
            return Response({"error": "Invalid Transaction ID"}, status=status.HTTP_404_NOT_FOUND)

        input_fields = []
  
        if transaction.current_stage == 1:
            input_fields = {
                "amount": {
                    "type": "decimal",
                    "min_value": 0,
                    "max_digits": 12,
                    "decimal_places": 2,
                    "required": True,
                }
            }
        elif transaction.current_stage == 2:
            input_fields = ["confirm_button"]

    
        return Response({
            "transaction_id": str(transaction.transaction_id),
            "current_stage": transaction.current_stage,
            "total_stages" : transaction.total_stages,
            "status": transaction.status,
            "input_fields": input_fields
        })