from rest_framework.viewsets import ModelViewSet
from categories.models import Category
from categories.serializers import CategorySerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

class CategoryView(ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated,)
    queryset = Category.objects.all()
    http_method_names = ["get", "post", "put", "delete"]

    def retrieve(self, request, pk=None):
        queryset = Category.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = CategorySerializer(user)
        return Response(serializer.data)


    def list(self, request, *args, **kwargs):
        profiles = Category.objects.all()
        serializer = CategorySerializer(profiles, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        pass

    def update(self, request, *args, **kwargs):
        pass

    def destroy(self, request, *args, **kwargs):
        pass