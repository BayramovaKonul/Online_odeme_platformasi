from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from phonenumbers import parse, format_number, NumberParseException, PhoneNumberFormat
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager
from ..validators import validate_phone_number
from .user_groups import UserGroupModel

def get_default_group():
    # Get or create the 'Standard' group (you can modify this to fit your logic)
    standard_group, _ = UserGroupModel.objects.get_or_create(name=UserGroupModel.STANDARD)
    return standard_group

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where phone number is the unique identifier
    for authentication instead of usernames (default version).
    """
    def create_user(self, phone_number, name, surname, password, **extra_fields):

        if not phone_number:
            raise ValueError("The Phone number must be set")
        if not name:
            raise ValueError("The Name must be set")
        if not surname:
            raise ValueError("The Surname must be set")
        
        # Validate and normalize the phone number
        #phone_number = validate_phone_number(phone_number)
        user = self.model(phone_number=phone_number, name=name, surname=surname, **extra_fields)
        # hash password
        user.set_password(password) 
        user.save()
        return user

    def create_superuser(self, phone_number, name, surname, password, **extra_fields):
    
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(phone_number, name, surname, password, **extra_fields)
    
    
class CustomUserModel(AbstractBaseUser, PermissionsMixin):
    phone_number=PhoneNumberField(region="AZ",unique=True, db_index=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    group = models.ForeignKey(UserGroupModel, on_delete=models.SET_NULL, null=True, blank=True, default=get_default_group, related_name='users')

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["name", "surname"]

    objects = CustomUserManager()

    class Meta:
        db_table = 'user'
        verbose_name ='User'
        verbose_name_plural ='Users'

    def __str__(self):
        return '{} {} - {}'.format(self.name, self.surname, self.phone_number)
