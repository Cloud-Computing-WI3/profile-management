from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from dj_rest_auth.registration.serializers import SocialLoginSerializer, RegisterSerializer
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.settings import api_settings
from rest_framework import serializers
from django.contrib.auth.models import Group
from .models import Account, Category, Keyword

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name",)
        extra_kwargs = {
            "name": {"validators": []},
        }

class KeywordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Keyword
        fields = ("id", "name",)
        extra_kwargs = {
            "name": {"validators": []},
        }


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ("id", "name",)
        extra_kwargs = {
            "name": {"validators": []},
        }


class AccountSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True, required=False)
    keywords = KeywordSerializer(many=True, required=False)
    categories = CategorySerializer(many=True, required=False)

    class Meta:
        model = Account
        fields = [
            "id", "email", "given_name", "family_name", "picture", "is_staff", "is_superuser", "date_joined",
            "groups", "categories", "keywords"
        ]

    def update(self, instance, validated_data):
        initial_groups = instance.groups.all()
        if "groups" in validated_data:
            groups_data = validated_data.pop("groups")
            for group in initial_groups:
                if group.name not in  [g["name"] for g in groups_data]:
                    instance.groups.remove(group)
            for group in groups_data:
                if not Group.objects.filter(name=group["name"]).exists():
                    g = Group.objects.create(name=group["name"])
                    instance.groups.add(g)

        instance.email = validated_data.get("email", instance.email)
        instance.given_name = validated_data.get("given_name", instance.given_name)
        instance.family_name = validated_data.get("family_name", instance.family_name)
        instance.is_staff = validated_data.get("is_staff", instance.is_staff)
        instance.is_superuser = validated_data.get("is_superuser", instance.is_superuser)
        instance.picture = validated_data.get("picture", instance.picture)
        instance.save()
        return instance


class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        data["user"] = AccountSerializer(self.user).data

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)
        data["refresh_token"] = data.pop("refresh")
        data["access_token"] = data.pop("access")
        return data

class GoogleLoginSerializer(SocialLoginSerializer):
    account = AccountSerializer(required=False)

    def get_cleaned_data(self):
        data_dict = super().get_cleaned_data()
        return data_dict
    def validate(self, attrs):
        attrs = super().validate(attrs)
        account = AccountSerializer(attrs["user"]).data
        attrs["acc"] = account

        return attrs

class RegistrationSerializer(AccountSerializer):
    given_name = serializers.CharField(required=True, min_length=1)
    family_name = serializers.CharField(required=True, min_length=1)
    picture = serializers.ImageField(default=None, required=False, allow_null=True)
    password = serializers.CharField(max_length=128, min_length=8, write_only=True, required=True)
    password2 = serializers.CharField(max_length=128, min_length=8, write_only=True, required=True)
    email = serializers.EmailField(required=True, write_only=True, max_length=128)

    class Meta:
        model = Account
        fields = ["id", "email", "given_name", "family_name", "picture", "password", "password2" ]

    def create(self, validated_data):
        if Account.objects.filter(email=validated_data["email"]).exists():
            raise serializers.ValidationError({"email": "This email is taken."})
        password = validated_data.pop("password")
        password2 = validated_data.pop("password2")
        account = Account(
            **validated_data,
        )
        if password != password2:
            raise serializers.ValidationError({"password": "Passwords must match."})
        account.set_password(password)
        account.save()
        return account
