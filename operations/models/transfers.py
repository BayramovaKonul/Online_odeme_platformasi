from django.db import models
import uuid
from account.models import CustomUserModel
from django.core.exceptions import ValidationError

class TransferTransactionModel(models.Model):
    STATUS_CHOICES = [
        ('pending_account', 'Pending Account'),
        ('pending_amount', 'Pending Amount'),
        ('pending_confirmation', 'Pending Confirmation'),
        ('completed', 'Completed'),
    ]

    sender = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE, related_name="transfer_sender")
    receiver = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE, related_name="transfer_receiver")
    transaction_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    transaction_type= models.CharField(max_length=50, default="transfer")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending_account')
    created_at = models.DateTimeField(auto_now_add=True) 
    completed_at = models.DateTimeField(null=True, blank=True) 


    class Meta:
        db_table = 'transfers'
        verbose_name ='Transfer Transaction'
        verbose_name_plural ='Transfer Transactions'
    
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

    def clean(self):
        """Validation: Ensure amount is positive and does not exceed sender's balance."""
        if self.amount is not None and self.amount < 0:
            raise ValidationError("Amount must be greater than or equal to zero.")
        if self.amount and self.sender.balance < self.amount:
            raise ValidationError("Insufficient balance for transfer.")

    def save(self, *args, **kwargs):
        """Apply validation before saving."""
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Transaction {self.transaction_id} - {self.status}"
