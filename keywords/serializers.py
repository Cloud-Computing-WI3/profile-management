from rest_framework import serializers
from keywords.models import Keyword
class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = ("id", "name",)