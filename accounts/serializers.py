from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from dj_rest_auth.registration.serializers import SocialLoginSerializer
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.settings import api_settings
from rest_framework import serializers
from django.contrib.auth.models import Group
from .models import Account
from categories.models import Category
from keywords.models import Keyword


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
    picture = serializers.FileField(required=False)

    class Meta:
        model = Account
        fields = [
            "id", "email", "given_name", "family_name", "picture", "is_staff", "is_superuser", "date_joined",
            "groups", "categories", "keywords"
        ]

    def update(self, instance, validated_data):
        # store the initial groups, keywords, and categories associated with the instance
        initial_groups = instance.groups.all()
        initial_keywords = instance.keywords.all()
        initial_categories = instance.categories.all()

        # if the "groups" key is present in the validated_data dictionary
        if "groups" in validated_data:
            # remove the groups data from the validated_data dictionary
            groups_data = validated_data.pop("groups")
            # iterate over the initial groups
            for group in initial_groups:
                # if the group name is not in the updated groups data
                if group.name not in [g["name"] for g in groups_data]:
                    # remove the group from the instance's groups
                    instance.groups.remove(group)
            # iterate over the updated groups data
            for group in groups_data:
                # if a group with the same name does not already exist in the database
                if not Group.objects.filter(name=group["name"]).exists():
                    # create a new group with the provided name
                    g = Group.objects.create(name=group["name"])
                else:
                    # otherwise, retrieve the existing group from the database
                    g = Group.objects.get(name=group["name"])
                # add the group to the instance's groups
                instance.groups.add(g)
        # If the "keywords" key is present in the validated_data dictionary
        if "keywords" in validated_data:
            # remove the keywords data from the validated_data dictionary
            keywords_data = validated_data.pop("keywords")
            # iterate over the initial keywords
            for keyword in initial_keywords:
                # if the keyword name is not in the updated keywords data
                if keyword.name not in [k["name"] for k in keywords_data]:
                    # remove the keyword from the instance's keywords
                    instance.keywords.remove(keyword)
            # iterate over the updated keywords data
            for keyword in keywords_data:
                # if a keyword with the same name does not already exist in the database
                if not Keyword.objects.filter(name=keyword["name"]).exists():
                    # create a new keyword with the provided name
                    k = Keyword.objects.create(name=keyword["name"])
                else:
                    # otherwise, retrieve the existing keyword from the database
                    k = Keyword.objects.get(name=keyword["name"])
                # add the keyword to the instance's keywords
                instance.keywords.add(k)

        # If the "categories" key is present in the validated_data dictionary
        if "categories" in validated_data:
            # remove the categories data from the validated_data dictionary
            categories_data = validated_data.pop("categories")

            # iterate over the initial categories
            for category in initial_categories:

                # if the category name is not in the updated categories data
                if category.name not in [c["name"] for c in categories_data]:
                    # remove the category from the instance's categories
                    instance.categories.remove(category)

            # iterate over the updated categories data
            for category in categories_data:
                # if a category with the same name does not already exist in the database
                if not Category.objects.filter(name=category["name"]).exists():
                    # create a new category with the provided name
                    c = Category.objects.create(name=category["name"])
                else:
                    # otherwise, retrieve the existing category from the database
                    c = Category.objects.get(name=category["name"])
                # add the category to the instance's categories
                instance.categories.add(c)

        # save other data from validated dict
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
        # call the parent class's validate method and store the returned data
        data = super().validate(attrs)

        # add the serialized user object to the data
        data["user"] = AccountSerializer(self.user).data

        # check if the 'UPDATE_LAST_LOGIN' attribute is set to True in settings.py, if true, call the 'update_last_login' function
        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)
        # rename the 'refresh' token to 'refresh_token'
        data["refresh_token"] = data.pop("refresh")
        # rename the 'access' token to 'access_token'
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
        fields = ["id", "email", "given_name", "family_name", "picture", "password", "password2"]

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
