import logging
from requests import Request

from django.conf import settings

from apps.core.utils import mail_sender, generate_password_reset_token, get_full_domain
from apps.core.constants import REGISTER_TOKEN_TYPE, RESEND_TOKEN, FORGET_PASSWORD_TOKEN_TYPE
from apps.core.utils import generate_opt

logger = logging.getLogger(__name__)


class EmailEvents:

    @staticmethod
    def send_invite_mail(user, *args, **kwargs):
        if user.is_active:
            return
        uid, token = generate_password_reset_token(user)
        subject = kwargs.get('subject') or "Invitation to join the project"
        context = {
            'email': user.email,
            'domain': f"{settings.DOMAIN}",
            'register_link': Request(
                'GET',f"{settings.HTTP_PROTOCOL}{kwargs.get('subdomain')}.{settings.DOMAIN}/set-password/?token={token}&uid={uid}"
                ).prepare().url,
            'first_name': user.first_name
        }

        try:
            mail_sender(
                template=f"email/invite_email.html",
                context=context,
                subject=subject,
                recipient_list=[user.email]
            )
        except Exception as e:
            logger.critical(e)
            logger.critical(f"Couldnot send email to invite user, {user.email}")

    
    @staticmethod
    def send_forget_password_email(user, *args, **kwargs):
        uid, token = generate_password_reset_token(user)
        logger.critical(f"sending email to , {user.email}")
        subject = kwargs.get('subject') or "Reset Password"
        otp_code = generate_opt(user, FORGET_PASSWORD_TOKEN_TYPE)

        context = {
            'email': user.email,
            'otp_code': otp_code,
            'first_name': user.first_name
        }
        logger.critical(f"Context: , {context}")

        try:
            logger.critical(f"Sending email:")
            a = mail_sender(
                template=f"email/forget_password.html",
                context=context,
                subject=subject,
                recipient_list=[user.email]
            )
            logger.critical(f"Status: , {a}")

        except Exception as e:
            logger.critical(f"Couldnot send email to user, {user.email}")

    
    @staticmethod
    def send_user_invite_mail(user, *args, **kwargs):
        request = kwargs.get('request')
        schema_name = request.headers.get('X-Schema-Name', '')
        subject = kwargs.get('subject') or "Welcome to the project"
        
        otp_code = generate_opt(user, REGISTER_TOKEN_TYPE)

        context = {
            'email': user.email,
            'domain': f"{settings.DOMAIN}",
            'otp_code': otp_code,
            'first_name': user.first_name
        }

        try:
            mail_sender(
                template=f"email/invite_email.html",
                context=context,
                subject=subject,
                recipient_list=[user.email]
            )
            logger.critical(f"Send mail success, {user.email}")


        except Exception as e:
            logger.critical(e)
            logger.critical(f"Couldnot send email to invite user, {user.email}")

    
    @staticmethod
    def resend_otp_code(user, *args, **kwargs):
        request = kwargs.get('request')
        schema_name = request.headers.get('X-Schema-Name', '')
        subject = kwargs.get('subject') or "Welcome to the project"
        
        otp_code = generate_opt(user, RESEND_TOKEN)

        context = {
            'email': user.email,
            'domain': f"{settings.DOMAIN}",
            'otp_code': otp_code,
            'first_name': user.first_name
        }

        try:
            mail_sender(
                template=f"email/invite_email.html",
                context=context,
                subject=subject,
                recipient_list=[user.email]
            )
            logger.critical(f"Send mail success, {user.email}")

        except Exception as e:
            logger.critical(e)
            logger.critical(f"Couldnot send email to invite user, {user.email}")