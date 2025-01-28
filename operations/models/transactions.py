from django.db import models
from account.models import CustomUserModel

class TransactionModel(models.Model):

    STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('completed', 'Completed'),
    ('failed', 'Failed'),
    ('canceled', 'Canceled')
]
 
    sender = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE, related_name="receiver")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status=models.CharField(choices=STATUS_CHOICES, default="pending")
    transaction_date = models.DateField(auto_now_add=True) 
    

    class Meta:
        db_table = 'transactions'
        verbose_name ='Transaction'
        verbose_name_plural ='Transactions'

    def __str__(self):
        return '{} - {}'.format(self.sender.phone_number, self.receiver.phone_number)
