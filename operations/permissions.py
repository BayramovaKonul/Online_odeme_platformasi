from rest_framework.permissions import BasePermission
from account.models import UserGroupModel

class IsGoldUserPermission(BasePermission):
    """
    Custom permission to allow only Gold users with the 'can_transfer' permission.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.group is not None  # Ensure user has a group assigned
            and request.user.group.name == UserGroupModel.GOLD  # Check if user is in 'gold' group
            and request.user.group.permissions.filter(codename="can_transfer_money").exists()  # Check if the group has 'can_transfer' permission
        )
