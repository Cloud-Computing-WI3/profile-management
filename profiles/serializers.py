from rest_framework import serializers
from django.contrib.auth.models import Group

from profiles.models import Profile


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    class Meta:
        model = Group
        fields = ("id", "name",)
        extra_kwargs = {
            "name": {"validators": []},
        }


class ProfileSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True, required=False)

    class Meta:
        model = Profile
        fields = (
            "id", "email", "first_name", "last_name", "avatar",
            "groups",
        )
    def create(self, validated_data):
        """
        Create and return a new `Profile` instance, given the validated data.
        """
        return Profile.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Profile` instance, given the validated data.
        """
        instance.email = validated_data.get("email", instance.email)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.save()
        return instance
