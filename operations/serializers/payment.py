from rest_framework import serializers
from ..models import PaymentTransactionModel, PaymentTypesModel, ProjectsModel
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from ..validators import validate_mobile_phone_number
from rest_framework import status, generics
from rest_framework.response import Response
from django.utils import timezone
from decimal import Decimal
from django.db.models import F

# class ChoosePaymentTypeSerializer(serializers.Serializer):

#     def create(self, validated_data):
#         request = self.context['request']
#         user = request.user  

#         # Get payment_type_id dynamically from the URL
#         payment_type_id = self.context.get('payment_type_id')  # Passed from the view
#         if not payment_type_id:
#             raise serializers.ValidationError({"payment_type": "Payment type is required."})

#         # Validate if payment_type exists
#         try:
#             payment_type = PaymentTypesModel.objects.get(id=payment_type_id)
#         except PaymentTypesModel.DoesNotExist:
#             raise serializers.ValidationError({"payment_type": "Invalid payment type."})

#         # Create the PaymentTransaction
#         transaction = PaymentTransactionModel.objects.create(
#             user=user,
#             value_type=payment_type.name.lower(),  
#             current_stage=1,
#             transaction_type="payment",
#         )
        
#         # Store transaction_id and payment_type_id in session
#         request.session['transaction_id'] = str(transaction.transaction_id)  
#         request.session['payment_type_id'] = str(payment_type.id)
#         self.context['transaction'] = transaction

#         # Store the serialized payment type (id, name) in the context
#         self.context['payment_type'] = {
#             "id": payment_type.id,
#             "name": payment_type.name
#         }

#         return transaction


# class ChooseProjectSerializer(serializers.Serializer):
    
#     def validate(self, data):
        
#         request = self.context['request']

#         # Retrieve session values
#         transaction_id = request.session.get('transaction_id')
#         payment_type_id = request.session.get('payment_type_id')

#         payment_type = get_object_or_404(PaymentTypesModel, id=payment_type_id)
#         transaction = get_object_or_404(PaymentTransactionModel, transaction_id=transaction_id, user=request.user)

#         if transaction.current_stage != 1:
#             return Response({'error': 'Invalid transaction stage'}, status=status.HTTP_400_BAD_REQUEST)
        
#         if not transaction_id:
#             raise serializers.ValidationError({"transaction_id": "Transaction ID is missing."})
#         if not payment_type_id:
#             raise serializers.ValidationError({"payment_type_id": "Payment type ID is missing."})


#         # Retrieve project_id from context (passed from the view)
#         project_id = self.context.get('project_id')
#         if not project_id:
#             raise serializers.ValidationError({"project_id": "Project ID is required."})

#         try:
#             project = ProjectsModel.objects.get(id=project_id, type=payment_type)
#         except ProjectsModel.DoesNotExist:
#             raise serializers.ValidationError({"project": "Invalid project."})

#         # Assign project to transaction and save
#         transaction.project = project
#         transaction.current_stage = 2
#         transaction.save()

#         request.session['project_id'] = str(project.id)

#         data["transaction"] = transaction  # Ensure updated transaction is returned
#         self.context['transaction'] = transaction

#         return data
    

# class CheckPaymentValueSerializer(serializers.Serializer):
#     value = serializers.CharField(max_length=100)
#     prefix = serializers.CharField(required=False)

#     def validate(self, data):
#         request = self.context['request']
        
#         value = data.get('value')
#         # Retrieve session values
#         transaction_id = request.session.get('transaction_id')
#         payment_type_id = request.session.get('payment_type_id')
#         project_id = request.session.get('project_id')

#         transaction = get_object_or_404(PaymentTransactionModel, transaction_id=transaction_id, user=request.user)
#         project=get_object_or_404(ProjectsModel,id=project_id)

#         if transaction.current_stage != 2:
#             return Response({'error': 'Invalid transaction stage'}, status=status.HTTP_400_BAD_REQUEST)


#         if not transaction_id:
#             raise serializers.ValidationError({"transaction_id": "Transaction ID is missing."})
#         if not payment_type_id:
#             raise serializers.ValidationError({"payment_type_id": "Payment type ID is missing."})
#         if not project_id:
#             raise serializers.ValidationError({"project_id": "Project ID is missing."})
        
#         if transaction.value_type == 'mobile':
#             prefix=data.get('prefix', None)
#             value = validate_mobile_phone_number(project, prefix, value)  
#             data['value'] = value

#         # Assign project to transaction and save
#         transaction.value = value
#         transaction.current_stage = 3
#         transaction.save()

#         request.session['value'] = str(value)

#         data["transaction"] = transaction  # Ensure updated transaction is returned
#         self.context['transaction'] = transaction

#         return data
    

# class CheckPaymentAmountSerializer(serializers.Serializer):
#     amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    
#     def validate_amount(self, amount):
#         value = amount
#         request = self.context['request']
#         user = request.user 
#         # Retrieve transaction from session
#         transaction_id = request.session.get('transaction_id')
#         transaction = get_object_or_404(PaymentTransactionModel, transaction_id=transaction_id, user=request.user)

#         if not transaction_id:
#             raise serializers.ValidationError("Transaction ID not found in session.")
        
#         transaction = get_object_or_404(PaymentTransactionModel, transaction_id=transaction_id)
#         # Ensure we are at stage 1
#         if transaction.current_stage != 3:
#             return Response({'error': 'Invalid transaction stage'}, status=status.HTTP_400_BAD_REQUEST)

#         if amount < 0:
#             raise serializers.ValidationError("The requested amount can not be less than zero")
        
#         if amount > user.balance:
#             raise serializers.ValidationError("The requested amount is more than your balance.")
        
#         # Update transaction
#         transaction.amount = amount
#         transaction.current_stage = 4 
#         transaction.save()

#         # Store amount in session
#         request.session['amount'] = str(amount)

#         self.context['transaction'] = transaction

#         return value


# class ConfirmPaymentSerializer(serializers.Serializer):

#     def save(self):

#         request = self.context['request']
#         amount = Decimal(request.session.get('amount'))

#         user = request.user

        
#         transaction_id = request.session.get('transaction_id')
#         payment_type_id = request.session.get('payment_type_id')
#         project_id = request.session.get('project_id')

#         current_transaction = get_object_or_404(PaymentTransactionModel, transaction_id=transaction_id, user=request.user)
        
#         if not transaction_id:
#             raise serializers.ValidationError({"transaction_id": "Transaction ID is missing."})
#         if not payment_type_id:
#             raise serializers.ValidationError({"payment_type_id": "Payment type ID is missing."})
#         if not project_id:
#             raise serializers.ValidationError({"project_id": "Project ID is missing."})
        
#         if current_transaction.current_stage != 4:
#             raise serializers.ValidationError("Invalid transaction stage")
  

#         user.__class__.objects.filter(pk=user.pk).update(balance=F('balance') - amount)
#         user.refresh_from_db()  # Refresh the user instance to get the updated balance
       

#         current_transaction.status = "completed"  
#         current_transaction.current_stage = 5  
#         current_transaction.completed_at=timezone.now()
#         current_transaction.save()
        

#         # Return response data with updated balances and transaction details
#         return {
#             "balance_after_payment": user.balance,
#             "transaction_type": "payment",
#             'payment_type': current_transaction.value_type,
#             "project": current_transaction.project.name,
#             "transaction_status": "completed",

#         }

        

class AddPaymentInputSerializer(serializers.Serializer):
    project = serializers.PrimaryKeyRelatedField(queryset=ProjectsModel.objects.all())
    payment_data = serializers.JSONField()

    def validate_payment_data(self, payment_data):
        """
        Validate payment_data dynamically based on project’s required inputs.
        If the payment type requires a phone number, apply the custom phone validation.
        """
        project = self.initial_data.get("project")  # Get project ID from request
        try:
            project_instance = ProjectsModel.objects.get(pk=project)
        except ProjectsModel.DoesNotExist:
            raise serializers.ValidationError("Invalid project.")

        required_fields = project_instance.type.required_inputs  # JSON structure

        # Ensure all required fields are provided
        for field_name, field_props in required_fields.items():
            if field_props.get("required", False) and field_name not in payment_data:
                raise serializers.ValidationError({field_name: "This field is required."})

            # Apply your existing phone number validation function
            if field_name == "phone_number" and field_props.get("type") == "string":
                prefix = payment_data.get("prefix", None)  # If we have prefix
                phone_number = payment_data[field_name]

                # Call existing function for validation
                valid_phone = validate_mobile_phone_number(project_instance, prefix, phone_number)
                payment_data[field_name] = valid_phone  # Store the validated phone number

        return payment_data


class AddPaymentAmountSerializer(serializers.Serializer):
    transaction_id = serializers.UUIDField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    def validate(self, data):
        print("Validate method called")
        """Ensure amount is positive and does not exceed sender’s balance."""
        transaction_id = data.get("transaction_id")
        amount = data.get("amount")

        print(transaction_id)

        try:
            transaction = PaymentTransactionModel.objects.get(transaction_id=transaction_id)
        except PaymentTransactionModel.DoesNotExist:
            raise serializers.ValidationError("Invalid Transaction ID")

        if amount <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        
        if transaction.user.balance < amount:
            raise serializers.ValidationError("Insufficient balance.")

        return data

class ConfirmPaymentSerializer(serializers.Serializer):
    transaction_id = serializers.UUIDField()





