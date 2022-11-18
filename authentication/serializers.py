from django.contrib.auth.models import update_last_login
from profiles.serializers import ProfileSerializer
from profiles.models import Profile
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.settings import api_settings

class RegistrationSerializer(ProfileSerializer):
    first_name = serializers.CharField(required=True, min_length=1)
    last_name = serializers.CharField(required=True, min_length=1)
    avatar = serializers.ImageField(default=None, required=False, allow_null=True)
    password = serializers.CharField(max_length=128, min_length=8, write_only=True, required=True)
    password2 = serializers.CharField(max_length=128, min_length=8, write_only=True, required=True)
    email = serializers.EmailField(required=True, write_only=True, max_length=128)

    class Meta:
        model = Profile
        fields = ["id", "first_name", "last_name", "email", "password", "password2", "is_active", "date_joined", "last_login", "avatar"]

    def create(self, validated_data):
        if Profile.objects.filter(email=validated_data["email"]).exists():
            raise serializers.ValidationError({"email": "This email is taken."})
        password = validated_data.pop("password")
        password2 = validated_data.pop("password2")
        account = Profile(
            **validated_data,
        )
        if password != password2:
            raise serializers.ValidationError({"password": "Passwords must match."})
        account.set_password(password)
        account.is_active = True
        account.save()
        return account


class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["user"] = ProfileSerializer(self.user).data

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data

class RefreshTokenSerializer(TokenRefreshSerializer):
    @classmethod
    def validate(self, attrs):
        data = super().validate(self, attrs)
        return data