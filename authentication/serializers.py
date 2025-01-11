from rest_framework import serializers
from .models import User
from .utils import send_password_reset_email


class UserRegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "username",
            "password",
            "confirm_password",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user = User.objects.create_user(**validated_data)
        return user


class EmailVerificationSerializer(serializers.Serializer):
    token = serializers.CharField(write_only=True)
    uid = serializers.CharField(write_only=True)

    class Meta:
        fields = ["token", "uid"]


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=255, write_only=True)
    username = serializers.CharField(max_length=255, read_only=True)
    access_token = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)
    id = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "username",
            "id",
            "access_token",
            "refresh_token",
        ]

    def validate(self, attrs):
        email = attrs.get("email", "")
        password = attrs.get("password", "")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"message": "User with this email does not exist."}
            )

        if not user.is_verified:
            raise serializers.ValidationError(
                {
                    "message": "Email is not verified.",
                }
            )

        if not user.check_password(password):
            raise serializers.ValidationError(
                {
                    "message": "Incorrect password.",
                }
            )
        print("WORKING")
        user_tokens = user.tokens()
        attrs["access_token"] = user_tokens["access"]
        attrs["refresh_token"] = user_tokens["refresh"]
        attrs["username"] = user.username
        attrs["id"] = user.id
        return attrs


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ["email"]

    def validate(self, attrs):
        email = attrs.get("email", "")

        if User.objects.filter(email=email).exists():
            send_password_reset_email(email)
        else:
            raise serializers.ValidationError(
                {"email": "User with this email does not exist."}
            )

        return super().validate(attrs)


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=255,
        write_only=True,
    )
    confirm_password = serializers.CharField(
        max_length=255,
        write_only=True,
    )
    uid = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)

    class Meta:
        fields = [
            "password",
            "confirm_password",
            "uid",
            "token",
        ]

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs
