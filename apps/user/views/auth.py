import logging

from django.conf import settings

from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN, \
    HTTP_401_UNAUTHORIZED, HTTP_500_INTERNAL_SERVER_ERROR

from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from rest_framework_simplejwt.exceptions import TokenError

from apps.core import utils
from apps.user.models import User, TokenVerification
from apps.user.serializers import LoginTokenSerializer, RefreshTokenSerializer, \
    ResetPasswordSerializer, ForgetPasswordSerializer
from apps.core.email_events import EmailEvents


logger = logging.getLogger(__name__)


class LoginView(TokenObtainPairView):
    serializer_class = LoginTokenSerializer

    def post(self, request, *args, **kwargs):
        user = User.objects.filter(email=request.data['email'])
        # , is_deleted=False, is_active=True
        if not user.exists():
            return Response({'message': "No active account found with the given credentials"},
                            status=HTTP_401_UNAUTHORIZED)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        return Response(serializer.data)


class RefreshTokenView(TokenRefreshView):
    serializer_class = RefreshTokenSerializer


class LogoutView(GenericAPIView):
    serializer_class = RefreshTokenSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except TokenError:
            pass
        return Response({'message': 'Successfully logged out.'})


class ForgotPasswordView(CreateAPIView):
    serializer_class = ForgetPasswordSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email', '')
        if not email:
            return Response({"error": "Email is not provided."}, status=HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email).first()
        if not user:
            return Response({"error": "User not found"}, status=HTTP_400_BAD_REQUEST)

        EmailEvents.send_forget_password_email(user, request=request)

        return Response({"message": "Password reset email has been sent. Please check your mail inbox."})


class ResetPasswordView(CreateAPIView):
    serializer_class = ResetPasswordSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'message': "Your password has reset successfully."})
