from django.db import models
from .user_model import User
from apps.core.models import TimestampMixin
from django.utils.translation import gettext_lazy as _
from apps.core.constants import USER_TOKEN_TYPES, REGISTER_TOKEN_TYPE, OTP_CODE_CHARS_POOL


class TokenVerification(TimestampMixin):
    code = models.CharField(null=True, blank=True)
    user = models.ForeignKey(User, related_name="token", on_delete=models.CASCADE)
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this code should be treated as active. '
        ),
    )
    expiring_time = models.DateTimeField(default=None, blank=True, null=True)
    type = models.CharField(choices=USER_TOKEN_TYPES, default=REGISTER_TOKEN_TYPE, null=True, blank=True, max_length=30)

    class Meta:
        db_table = 'token_verifications'

    @classmethod
    def generate_otp_code(cls) -> str:
        """ Generates and returns otp code """
        import random
        chars = list(OTP_CODE_CHARS_POOL)
        random.shuffle(chars)
        code = "".join(random.choices(chars, k=6))
        if cls.objects.filter(code=code).exclude(is_active=True).exists():
            cls.generate_otp_code()
        return code
