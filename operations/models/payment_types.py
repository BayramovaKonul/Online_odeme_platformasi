from django.db import models

class PaymentTypesModel(models.Model):

    name = models.CharField(max_length=100, unique=True)
    required_inputs = models.JSONField(default=dict)
    started_at = models.DateField(auto_now_add=True) 


    class Meta:
        db_table = 'payment_types'
        verbose_name ='Payment Type'
        verbose_name_plural ='Payment Types'

    def __str__(self):
        return self.name
