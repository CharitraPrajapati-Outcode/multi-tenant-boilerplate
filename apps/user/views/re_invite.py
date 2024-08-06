from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.status import HTTP_400_BAD_REQUEST

from ..models import User
from apps.core.email_events import EmailEvents
from rest_framework.views import APIView

class ReInviteUserView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.get(id=kwargs.get('id'))
        except User.DoesNotExist:
            return Response({
                'error': 'Invalid user id.'
            }, status=HTTP_400_BAD_REQUEST)
        else:
            if user.is_active:
                return Response({
                'error': 'Can\'t invite active user.'
            }, status=HTTP_400_BAD_REQUEST)
        
        EmailEvents.send_invite_mail(user=user, subject='Re-invitation to join the project', subdomain=request.get_host().split(':')[0].lower().split('.')[0])
        return Response({
            'message':'Re-invitation sent successfully.'
        })