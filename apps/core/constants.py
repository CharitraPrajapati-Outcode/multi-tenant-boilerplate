REGISTER_TOKEN_TYPE = 'register'
FORGET_PASSWORD_TOKEN_TYPE = 'forget_password'
RESEND_TOKEN = 'resend_token'
OTP_CODE_CHARS_POOL = "ABCDEFGHIJKLMNPQRSTUVWXYZ12345679"

USER_TOKEN_TYPES = (
    (FORGET_PASSWORD_TOKEN_TYPE, FORGET_PASSWORD_TOKEN_TYPE),
    (REGISTER_TOKEN_TYPE, REGISTER_TOKEN_TYPE),
    (RESEND_TOKEN, RESEND_TOKEN)
)