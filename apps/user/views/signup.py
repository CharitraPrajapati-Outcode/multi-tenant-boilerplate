from django.db import transaction

from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView

from apps.user.serializers import SignupSerializer, VerifyEmailSerializer, ForgetPasswordSerializer
from apps.user.models import User
from apps.core.email_events import EmailEvents
import logging

logger = logging.getLogger(__name__)


class SignupView(CreateAPIView):
    serializer_class = SignupSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        try:
            serializer.save()
        except Exception as error:
            return Response({
                'message': "Signup Failed. Please try again in a while",
                'error': str(error)}, status=HTTP_400_BAD_REQUEST)

        return Response({
            "message": "Signed up successfully. Enter OTP code sent to your email to login."
        }, status=HTTP_201_CREATED)
    

class VerifyEmail(CreateAPIView):
    serializer_class = VerifyEmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({
            "message": "Email verified successfully."
        })
    

class ResendOTPCode(CreateAPIView):
    serializer_class = ForgetPasswordSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = User.objects.get(email=serializer.data['email'])
            if user.is_verified:
                return Response({
                    "message": "Account already active."
                }, status=HTTP_400_BAD_REQUEST)
            EmailEvents.resend_otp_code(user, request=request)
        except User.DoesNotExist:
            return Response({
                "error": "User with this email doesn't exist."
            }, status=HTTP_400_BAD_REQUEST)
        
        return Response({
            "message": "OTP code sent successfully. Please check your email."
        })