from django.db import models
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

class UserGroupModel(models.Model):
    STANDARD = 'standard'
    GOLD = 'gold'

    GROUP_CHOICES = [
        (STANDARD, 'Standard'),
        (GOLD, 'Gold'),
    ]

    name = models.CharField(max_length=20, choices=GROUP_CHOICES, unique=True)
    permissions = models.ManyToManyField(Permission, blank=True, related_name="custom_groups")

    class Meta:
        db_table = 'custom_user_groups'
        verbose_name ='User-Group'
        verbose_name_plural ='User-Groups'

        permissions = [
            ("can_transfer_money", "Can transfer money"),
        ]

    def __str__(self):
        return self.name
    
