import logging

from django.conf import settings
from django.db import transaction

from rest_framework import serializers

from apps.user.models import User, UserProfile, TokenVerification
from apps.core.email_events import EmailEvents
from .auth import LoginTokenSerializer
from apps.core.constants import REGISTER_TOKEN_TYPE

logger = logging.getLogger(__name__)


class SignupSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=255)
    confirm_password = serializers.CharField(max_length=255)

    def to_representation(self, instance=None):
        serializer = LoginTokenSerializer(data=self.validated_data, context=self.context)
        serializer.is_valid()
        return serializer.data

    def validate(self, data):
        error = {}
        if not data['password'] == data['confirm_password']:
            error['confirm_password'] = "Passwords didn't match."
        
        if User.objects.filter(email=data['email']).exists():
            error['email'] = "User with this email exists."

        if error:
            raise serializers.ValidationError(error)

        data.pop('confirm_password')
        return data

    @transaction.atomic()
    def create(self, validated_data):
        email = validated_data.pop('email')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        password = validated_data.pop('password')

        try:
            logger.info("Creating User Instance for email " + email)
            user = User.objects.create_user(email=email, password=password,
                                            first_name=first_name, last_name=last_name)
            UserProfile.objects.create(user=user)
            
        except Exception as err:
            logger.warning(f"FailNo Environmented User instance; Error: {str(err)}")
            raise err
        
        EmailEvents.send_user_invite_mail(user, request=self.context.get("request"))
    
        logger.info(f"User {email} created successfully.")
        return user


class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        error = {}
        try:
            user_token = TokenVerification.objects.get(user__email=data['email'], code=data['code'])
            if user_token.user:
                user_token.user.is_verified = True
                user_token.user.save()
        except TokenVerification.DoesNotExist:
            error['code'] = "Invalid code."

        if error:
            raise serializers.ValidationError(error)

        return data