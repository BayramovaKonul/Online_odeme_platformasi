from ..serializers import UserRegisterSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

class RegisterUserView(APIView):
    permission_classes = [AllowAny]  # Allow access without authentication

    def post(self, request):
        serializer= UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)