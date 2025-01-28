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
    groups = models.ManyToManyField(Group, related_name='user_groups', blank=True)  # Link to the Group model

    class Meta:
        db_table = 'custom_user_groups'
        verbose_name ='User-Group'
        verbose_name_plural ='User-Groups'

        permissions = [
            ("can_transfer_money", "Can transfer money"),
        ]

    def __str__(self):
        return self.name
    
    # Custom method to assign permission to gold users
    def assign_permissions(self):
        if self.name == self.GOLD:
            permission = Permission.objects.get(codename='can_transfer_money')
            # Assign permission to all users in this group
            for user in self.groups.all():
                user.user_permissions.add(permission)
                user.save()
