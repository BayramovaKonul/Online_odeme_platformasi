from ..serializers import UserProfileUpdateSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


class UpdateUserProfile(APIView):
    def patch(self, request):
        print("Incoming request data:", request.data)  
        user_profile = request.user.profile # profile is a related name
        # Initialize the serializer
        serializer = UserProfileUpdateSerializer(instance=user_profile, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)