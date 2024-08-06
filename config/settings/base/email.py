from decouple import config

## Email Settings
EMAIL_BACKEND = config("EMAIL_BACKEND", default='django.core.mail.backends.console.EmailBackend')

FROM_EMAIL = config('FROM_EMAIL', default='info@domain.com')

EMAIL_HOST = config('EMAIL_HOST', default='')
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
EMAIL_PORT = config('EMAIL_PORT', default=587)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=False, cast=bool)
EMAIL_USE_SSL = config('EMAIL_USE_SSL', default=False, cast=bool)
EMAIL_TIMEOUT = 5

OTP_VERIFICATION_CODE_EXPIRY_TIME = config('EMAIL_PORT', cast=int, default=120)