import re
from rest_framework.exceptions import ValidationError
from account.models import CustomUserModel  

# Define the default prefixes for each mobile provider
DEFAULT_PREFIXES = {
    "Bakcell": "55",
    "Azercell": "50",
    "Nar": "77",
}

# Define allowed prefixes per provider
ALLOWED_PREFIXES = {
    "Bakcell": ["55", "90", "77", "51"],
    "Azercell": ["50", "51", "55", "70"],
    "Nar": ["77", "71", "79", "70"],
}

def validate_mobile_phone_number(project, prefix, value):
    """
    Validate the remaining part of the phone number (after the prefix).
    """
    # Ensure the provider exists
    if project.name not in DEFAULT_PREFIXES:
        raise ValidationError(f"Invalid provider '{project.name}'. Choose from: {', '.join(DEFAULT_PREFIXES.keys())}.")

    # Get the default prefix
    default_prefix = DEFAULT_PREFIXES[project.name]

    if not prefix:
        prefix = default_prefix  # Assign default prefix

    allowed_prefixes = ALLOWED_PREFIXES.get(project.name, [])
    if prefix not in allowed_prefixes:
        raise ValidationError(f"Invalid prefix '{prefix}' for provider '{project.name}'. Allowed: {', '.join(allowed_prefixes)}")

    
    # Ensure the user input is exactly 7 digits
    if not re.match(r'^\d{7}$', value):
        raise ValidationError("Invalid phone number. You must enter exactly 7 digits after the prefix.")

    # Create the full phone number
    full_phone_number = f"{prefix}{value}"

    # Ensure the full number starts with a valid prefix for the provider
    if not any(full_phone_number.startswith(p) for p in ALLOWED_PREFIXES[project.name]):
        raise ValidationError(f"Invalid phone number prefix for '{project.name}'. Allowed prefixes: {', '.join(ALLOWED_PREFIXES[project.name])}.")

    # # Check if the phone number already exists in the database
    # if CustomUserModel.objects.filter(phone_number=full_phone_number).exists():
    #     raise ValidationError(f"The phone number {full_phone_number} is already registered.")

    return full_phone_number
