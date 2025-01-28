from django.db import models
from autoslug import AutoSlugField

class ProjectsModel(models.Model):

    PROJECT_TYPE_CHOICES = [
    ('mobile', 'Mobile'),
    ('bank', 'Government Payments'),
    ('internet', 'Internet'),
    ('phone', 'Phone'),
    ('betting', 'Betting')
]
 
    name = models.CharField(max_length=100, unique=True)
    slug = AutoSlugField(populate_from="name")
    type = models.CharField(max_length=50, choices=PROJECT_TYPE_CHOICES)
    started_at = models.DateField(auto_now_add=True) 
    updated_at = models.DateField(auto_now=True) 

    class Meta:
        db_table = 'projects'
        verbose_name ='Project'
        verbose_name_plural ='Projects'

    def __str__(self):
        return '{} - {}'.format(self.name, self.type)
