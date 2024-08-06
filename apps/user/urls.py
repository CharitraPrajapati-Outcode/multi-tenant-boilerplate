from django.urls import path

from rest_framework.routers import SimpleRouter

from apps.user.views import LoginView, LogoutView, RefreshTokenView, \
    ResetPasswordView, ForgotPasswordView, SignupView, AccountProfileView, \
    UpdatePasswordView, ListUserView, GetUserView, VerifyEmail, \
    ResendOTPCode


router = SimpleRouter(trailing_slash=False)

urlpatterns = router.urls

urlpatterns += [
    path('auth/login', LoginView.as_view(), name="login"),
    path('auth/signup', SignupView.as_view(), name="signup"),
    path('auth/logout', LogoutView.as_view(), name="logout"),
    path('auth/refresh', RefreshTokenView.as_view(), name="refresh-token"),
    path('auth/forgot-password', ForgotPasswordView.as_view(), name="forgot-password"),
    path('auth/reset-password', ResetPasswordView.as_view(), name="reset-password"),
    path('auth/update-password', UpdatePasswordView.as_view(), name='update-password'),

    path('account-profile', AccountProfileView.as_view(), name='account-profile'),

    path('auth/verify-email', VerifyEmail.as_view(), name="verify-token"),
    path('auth/resend-otp-code', ResendOTPCode.as_view(), name="resend-otp-code"),
]

app_name = 'user'