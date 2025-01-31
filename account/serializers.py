import re
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import CustomUserModel, UserProfileModel
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import ValidationError
from django.contrib.auth.hashers import check_password

class UserRegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, validators=[validate_password])  # Apply strong password validation
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUserModel
        fields = ['phone_number', 'name', 'surname', 'password1', 'password2']

    def validate(self, data):
        phone_number = data.get('phone_number')
        password1 = data.get('password1')
        password2 = data.get('password2')

    
        if CustomUserModel.objects.filter(phone_number=phone_number).exists():
            raise serializers.ValidationError({"phone_number": "This phone number is already registered."})


        if password1 != password2:
            raise serializers.ValidationError({"password2": "Passwords must match."})


        data['password'] = make_password(password1)
        data.pop('password1')
        data.pop('password2')
        return data

    def validate_phone_number(self, value):
        """Validates and normalizes Azerbaijani phone numbers."""
        original_value = value.strip().replace(" ", "") 

        patterns = [
            r"^\+994(50|51|55|70|77|99)\d{7}$",  # Format: +994XXXXXXXXX
            r"^0(50|51|55|70|77|99)\d{7}$",      # Format: 05XXXXXXXX
            r"^(50|51|55|70|77|99)\d{7}$"        # Format: 5XXXXXXXX
        ]

        if any(re.match(pattern, original_value) for pattern in patterns):

            if original_value.startswith("0"):  
                return "+994" + original_value[1:]  # Convert `055XXXXXXX` → `+99455XXXXXXX`
            elif not original_value.startswith("+994"):  
                return "+994" + original_value  # Convert `558888888` → `+994558888888`
            return original_value  

        raise serializers.ValidationError("Invalid phone number format. Use +994XXXXXXXXX, 05XXXXXXXX, or 5XXXXXXXX.")

        
class UserBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUserModel
        fields = ['name', 'surname']

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    user = UserBaseSerializer()
 
    class Meta:
        model= UserProfileModel
        fields =['birthday', 'address', 'email', 'user']


    def update(self, instance, validated_data):
        # Extract nested user data and collect them together
        user_data = validated_data.pop('user', None)
        print(user_data)
        
        # print(user_data)
        
        # Update the UserProfileModel instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update the related CustomUserModel instance
        if user_data:
            custom_user = instance.user  # Get the associated CustomUser instance
            custom_user.name = user_data.get('name', custom_user.name)
            custom_user.surname = user_data.get('surname', custom_user.surname)
            custom_user.save()

        return instance

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        
        # Normalize the phone number
        normalized_phone = self.normalize_phone_number(phone_number)
        
        if not normalized_phone:
            raise ValidationError("Invalid phone number format. Use +994XXXXXXXXX, 05XXXXXXXX, or 5XXXXXXXX.")
        
        # Authenticate using the normalized phone number
        try:
            user = CustomUserModel.objects.get(phone_number=normalized_phone)
        except CustomUserModel.DoesNotExist:
            raise ValidationError("No account found with this phone number.")
        
        # Proceed to authenticate with the user and token
        attrs['phone_number'] = normalized_phone  # Replace the input with the normalized one
        return super().validate(attrs)

    def normalize_phone_number(self, value):
        """Normalize phone number to +994XXXXXXXXX format."""
        value = value.strip().replace(" ", "")  
        
        if value.startswith("0"): 
            return "+994" + value[1:]  
        elif value.startswith("5"): 
            return "+994" + value  
        elif value.startswith("+994"): 
            return value
        return None 


class ResetPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True, min_length=8)
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate_old_password(self, value):
        user = self.context.get('user')

        if not check_password(value, user.password):
            raise serializers.ValidationError("The old password is incorrect.")
        return value

    def validate(self, data):
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')

        if new_password != confirm_password:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return data

    def save(self, **kwargs):
        user = self.context.get('user') 
        user.set_password(self.validated_data['new_password'])
        user.save()


