from django.contrib.auth.models import update_last_login
from profiles.serializers import ProfileSerializer
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.settings import api_settings


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
    pk = serializers.IntegerField(required=True)
    @classmethod
    def validate(self, attrs):
        data = super().validate(self, attrs)
        data["pk"] = attrs["pk"]
        return data