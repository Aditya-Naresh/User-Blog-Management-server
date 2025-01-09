from django.urls import path
from . import views

urlpatterns = [
    path(
        "register/",
        views.RegisterView.as_view(),
        name="register",
    ),
    path(
        "email-verify/",
        views.EmailVerificationView.as_view(),
        name="email-verify",
    ),
    path(
        "login/",
        views.LoginView.as_view(),
        name="login",
    ),
    path(
        "forgot-password/",
        views.ForgotPasswordView.as_view(),
        name="forgot-password",
    ),
    path(
        "reset-password/",
        views.ResetPasswordView.as_view(),
        name="reset-password",
    ),
]
