from django.db import models
from autoslug import AutoSlugField
from .payment_types import PaymentTypesModel

class ProjectsModel(models.Model):

    name = models.CharField(max_length=100, unique=True)
    type = models.ForeignKey(PaymentTypesModel, on_delete=models.CASCADE, related_name="projects")
    started_at = models.DateField(auto_now_add=True) 
    updated_at = models.DateField(auto_now=True) 

    class Meta:
        db_table = 'projects'
        verbose_name ='Project'
        verbose_name_plural ='Projects'

    def __str__(self):
        return '{} - {}'.format(self.name, self.type)
