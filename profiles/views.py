from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from profiles.models import Profile
from profiles.serializers import ProfileSerializer


class ProfileView(ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = (AllowAny,)
    queryset = Profile.objects.all()
    http_method_names = ["get", "post", "put", "delete"]

    def list(self, request, *args, **kwargs):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        pass

    def update(self, request, *args, **kwargs):
        pass

    def destroy(self, request, *args, **kwargs):
        pass
