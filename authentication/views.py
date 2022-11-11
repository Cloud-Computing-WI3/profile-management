from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from authentication.serializers import LoginSerializer, RefreshTokenSerializer
from profiles.models import Profile
from profiles.serializers import ProfileSerializer

class LoginViewSet(ModelViewSet, TokenObtainPairView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)
    http_method_names = ["post"]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class RefreshViewSet(ViewSet, TokenRefreshView):
    permission_classes = (AllowAny,)
    http_method_names = ["post"]
    data = {}
    def create(self, request, *args, **kwargs):
        serializer = RefreshTokenSerializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            if serializer.is_valid():
                access_token = serializer.validated_data["access"]
                user = ProfileSerializer(instance=Profile.objects.get(pk=int(serializer.validated_data["pk"])))
                data = {
                    "access": access_token,
                    "user": user.data
                }
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(data, status=status.HTTP_200_OK)