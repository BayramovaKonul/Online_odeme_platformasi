from phonenumbers import parse, is_valid_number, format_number, PhoneNumberFormat
from phonenumbers.phonenumberutil import NumberParseException
from django.core.exceptions import ValidationError

def validate_phone_number(value):
    """
    Validates and normalizes a phone number. Ensures it has a valid format
    and adds the default country code if not provided.
    """
    try:
        # Attempt to parse the phone number with a default region (e.g., "AZ" for Azerbaijan)
        parsed_number = parse(value, "AZ")

        # Check if the number is valid
        if not is_valid_number(parsed_number):
            raise ValidationError(f"Invalid phone number: {value}")

        # Format the number to E.164 format (e.g., +994558686404)
        return format_number(parsed_number, PhoneNumberFormat.E164)
    except NumberParseException:
        raise ValidationError(f"Invalid phone number: {value}")
