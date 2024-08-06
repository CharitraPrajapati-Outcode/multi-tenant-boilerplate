from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from apps.user.models import User, TokenVerification
from apps.core.constants import FORGET_PASSWORD_TOKEN_TYPE

class LoginTokenSerializer(TokenObtainPairSerializer):

    def to_representation(self, instance):
        response = self.validated_data
        response['id'] = self.user.id
        return response


class RefreshTokenSerializer(TokenRefreshSerializer):
    def save(self):
        refresh = self.context['request'].data.get('refresh', '')
        RefreshToken(refresh).blacklist()


class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=100)
    confirm_password = serializers.CharField(max_length=100)
    code = serializers.CharField()
    email = serializers.EmailField()

    def validate(self, data):
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError({
                'email': ['Invalid email address.']
            })
        if not data['new_password'] == data['confirm_password']:
            raise serializers.ValidationError({'confirm_password': ["Passwords didn't match."]})
        try:
            TokenVerification.objects.get(user=user, code=data['code'], type=FORGET_PASSWORD_TOKEN_TYPE)
        except TokenVerification.DoesNotExist:
            raise serializers.ValidationError({'code': ['Invalid OTP code.']})
        # import re
        # if not re.match(r"^(?=.*[A-Za-z])(?=.*[0-9])(?=.*[!@#$%^&*_+=\\<>?,./-]).{8,}$",
        #                 data['new_password']):
        #     raise serializers.ValidationError(
        #         {'password': [
        #             "Password must contain at least 8 characters with one number and one special character."
        #         ]})
        return data

    def create(self, validated_data):
        user = User.objects.get(email=validated_data.get('email'))
        user.set_password(validated_data['new_password'])
        user.save()
        return True
