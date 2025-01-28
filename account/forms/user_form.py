from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from ..models import CustomUserModel
from django import forms
from phonenumbers import parse, format_number, NumberParseException, PhoneNumberFormat

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUserModel
        fields = ("phone_number", "name", "surname")

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUserModel
        fields = ("phone_number", "name", "surname")
