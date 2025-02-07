from django.db import models
from autoslug import AutoSlugField
from .projects import ProjectsModel
from account.models import CustomUserModel
import uuid
class PaymentTransactionModel(models.Model):

    class StatusChoices(models.TextChoices):
        PENDING = 'pending', 'Pending'
        COMPLETED = 'completed', 'Completed'
        FAILED = 'failed', 'Failed'

    user=models.ForeignKey(CustomUserModel, on_delete=models.CASCADE, related_name="payments")
    project = models.ForeignKey(ProjectsModel, on_delete=models.SET_NULL, null=True, related_name="payments")
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    current_stage = models.IntegerField(default=0)
    total_stages = models.IntegerField(default=3)
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.PENDING)
    transaction_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    transaction_type= models.CharField(max_length=50, default="payment")
    payment_data = models.JSONField(default=dict) 
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 
    completed_at = models.DateTimeField(null=True, blank=True) 

    class Meta:
        db_table = 'payment_transactions'
        verbose_name ='Payment Transaction'
        verbose_name_plural ='Payment Transactions'

    def __str__(self):
        return '{} - {}'.format(self.user, self.project)
