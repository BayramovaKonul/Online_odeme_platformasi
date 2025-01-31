from ..serializers import ResetPasswordSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

class PasswordResetView(APIView):
    def post(self, request):
        user=request.user
        serializer = ResetPasswordSerializer(data=request.data, context={'user': user})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password reset successful."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)