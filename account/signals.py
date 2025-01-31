
# code
from django.db.models.signals import post_save, pre_delete

from django.dispatch import receiver
from .models import CustomUserModel, UserProfileModel
 
 
@receiver(post_save, sender=CustomUserModel) 
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfileModel.objects.create(user=instance)
