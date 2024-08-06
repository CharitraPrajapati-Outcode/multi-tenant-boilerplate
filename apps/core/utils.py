import logging
from datetime import timedelta

from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from celery import shared_task

from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from apps.user.models import User, TokenVerification
from .constants import REGISTER_TOKEN_TYPE, FORGET_PASSWORD_TOKEN_TYPE, RESEND_TOKEN, FORGET_PASSWORD_TOKEN_TYPE

logger = logging.getLogger(__name__)


@shared_task
def mail_sender(template, context, subject, recipient_list):
    message = render_to_string(template, context)
    a = send_mail(subject=subject, message='',
              from_email=getattr(settings, 'FROM_EMAIL', ''),
              recipient_list=recipient_list,
              html_message=message)


def generate_password_reset_token(user):
    from django.utils.encoding import force_bytes
    from django.utils.http import urlsafe_base64_encode

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = PasswordResetTokenGenerator().make_token(user)

    return uid, token


def check_reset_token(user, token):
    return PasswordResetTokenGenerator().check_token(user, token)


def get_full_domain(request):
    hostname = request.get_host().split(':')[0].lower()
    if len(hostname.split('.')) == 2:
        subdomain_prefix = hostname.split('.')[0]
        return settings.HTTP_PROTOCOL + subdomain_prefix + '.' + settings.DOMAIN
    else:
        return settings.HTTP_PROTOCOL + settings.DOMAIN
    

def generate_opt(user, otp_type):
    expiring_time = timezone.now() + timedelta(seconds=getattr(settings, 'OTP_VERIFICATION_CODE_EXPIRY_TIME'))
    otp_code = TokenVerification.generate_otp_code()

    if otp_type == REGISTER_TOKEN_TYPE:
        TokenVerification.objects.create(
            user=user,
            type=otp_type,
            expiring_time=expiring_time,
            is_active=True,
            code=otp_code
        )
    if otp_type in [RESEND_TOKEN, FORGET_PASSWORD_TOKEN_TYPE]:
        verification_token = TokenVerification.objects.filter(user=user, type=otp_type)
        if verification_token.exists():
            verification_token.update(is_active=True, expiring_time=expiring_time, code=otp_code)
        else:
            TokenVerification.objects.create(
                user=user,
                type=otp_type,
                expiring_time=expiring_time,
                is_active=True,
                code=otp_code
            )
   
    return otp_code