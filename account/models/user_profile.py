from django.db import models
from .user import CustomUserModel
from django.contrib.auth import get_user_model

User= get_user_model()

class UserProfileModel(models.Model):
    birthday=models.DateField(null=True, blank=True)
    email=models.EmailField(null=True, blank=True)
    address=models.CharField(max_length=255, null=True, blank=True)
    user=models.OneToOneField(CustomUserModel, on_delete=models.CASCADE,
                             related_name="profile")

    class Meta:
        db_table='user_profile'
        verbose_name='User_profile'
        verbose_name_plural='User_profiles'

    def __str__(self):
        return f"{self.user.name}"