from rest_framework.viewsets import ModelViewSet
from keywords.models import Keyword
from keywords.serializers import KeywordSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

class KeywordView(ModelViewSet):
    serializer_class = KeywordSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Keyword.objects.all()
    http_method_names = ["get", "post", "put", "delete"]

    def retrieve(self, request, pk=None):
        queryset = Keyword.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = KeywordSerializer(user)
        return Response(serializer.data)


    def list(self, request, *args, **kwargs):
        profiles = Keyword.objects.all()
        serializer = KeywordSerializer(profiles, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        pass

    def update(self, request, *args, **kwargs):
        pass

    def destroy(self, request, *args, **kwargs):
        pass