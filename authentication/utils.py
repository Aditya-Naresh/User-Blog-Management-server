from django.contrib.auth.tokens import (
    default_token_generator,
    PasswordResetTokenGenerator,
)
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings
from django.core.mail import EmailMessage
import environ
from .models import User

env = environ.Env()
environ.Env.read_env()

FRONTEND_URL = env("FRONTEND_URL")


def send_verification_email(user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise ValueError("User creation error")
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.id))
    verification_link = f"{FRONTEND_URL}/verify-email/{uid}/{token}"
    message = f"""
    Hi {user.username},\n
    Please verify your email address by clicking the link below.
    {verification_link}\n
    If you didn't create an account with us, please ignore this email.\n
    Thank you.
    """
    email = EmailMessage(
        subject="Email Verification",
        body=message,
        from_email=settings.EMAIL_HOST_USER,
        to=[user.email],
    )

    email.send(fail_silently=False)
    print("Email sent successfully")


def send_password_reset_email(email):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        raise ValueError({"email": "User with this email does not exist."})

    token = PasswordResetTokenGenerator().make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.id))
    password_reset_link = f"{FRONTEND_URL}/reset-password/{uid}/{token}"
    message = f"""
    Hi {user.username},\n
    Please reset your password by clicking the link below.
    {password_reset_link}\n
    If you didn't request a password reset, please ignore this email.
    Thank you.
    """
    email = EmailMessage(
        subject="Password Reset",
        body=message,
        from_email=settings.EMAIL_HOST_USER,
        to=[user.email],
    )
    email.send(fail_silently=False)
