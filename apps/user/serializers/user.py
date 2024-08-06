import logging

from rest_framework import serializers

from django.db import transaction

from apps.user.models import User, UserProfile

logger = logging.getLogger(__name__)


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('image',)


class UserBasicSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(source='profile.image', allow_null=True, required=False)
    
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'image', 'is_verified')
        read_only_fields = ('id', 'email', 'is_verified')

    def to_representation(self, instance):
        response = super().to_representation(instance)

        return response
    
    def update(self, instance, validated_data):
        if validated_data.get('first_name'):
            instance.first_name = validated_data.get('first_name')
        if validated_data.get('last_name'):
            instance.last_name = validated_data.get('last_name')
        instance.save()
        image = validated_data.get('profile', {}).get('image', None)
        user_profile = instance.profile
        user_profile.image=image
        user_profile.save()

        return self.data
   

class PasswordUpdateSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate(self, attrs):
        if attrs.get('new_password') != attrs.get('confirm_password'):
            raise serializers.ValidationError('Confirm password is not same as new password.')

        user = self.context.get('user')
        if not user.check_password(attrs.get('old_password')):
            raise serializers.ValidationError('Enter correct old password.')
        
        return attrs
