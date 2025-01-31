from django.db import models
from account.models import CustomUserModel

class TransactionModel(models.Model):

    STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('completed', 'Completed'),
    ('failed', 'Failed'),
]
 
    sender = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE, related_name="receiver", null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type= models.CharField(max_length=50)
    status=models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    current_stage = models.IntegerField(default=0)
    created_at = models.DateField(auto_now_add=True) 
    completed_at = models.DateField(null=True, blank=True) 
    

    class Meta:
        db_table = 'transactions'
        verbose_name ='Transaction'
        verbose_name_plural ='Transactions'

    def __str__(self):
        return '{} - {}'.format(self.sender.phone_number, self.receiver.phone_number)
