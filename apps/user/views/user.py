from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView, RetrieveAPIView
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN, HTTP_200_OK, HTTP_404_NOT_FOUND
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser, FormParser

from apps.user.serializers import UserBasicSerializer, PasswordUpdateSerializer, UserProfileSerializer
from apps.user.models import User, UserProfile


class AccountProfileView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserBasicSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self):
        return self.request.user
    

class UpdatePasswordView(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = PasswordUpdateSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = self.serializer_class(data=request.data, context={'user': user})
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.validated_data.get('new_password'))
        user.save()
        return Response({
            'message': 'Password updated successfully.'
        })


class ListUserView(ListAPIView):
    serializer_class = UserBasicSerializer
    queryset = User.objects.filter(is_deleted=False)


class GetUserView(APIView):

    def get(self, request, *args, **kwargs):
        uid = kwargs.get('uid')
        
        from django.utils.encoding import force_str
        from django.utils.http import urlsafe_base64_decode

        uid = force_str(urlsafe_base64_decode(uid))
        try:
            user = User.objects.get(id=uid)
        except Exception:
            return Response({'message': "Requested user not found."}, status=HTTP_403_FORBIDDEN)

        return Response({
            'email': user.email
        }, status=HTTP_200_OK)
