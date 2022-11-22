from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from accounts.serializers import LoginSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework.response import Response
from rest_framework import status
from accounts.serializers import GoogleLoginSerializer

class GoogleAuthAdapter(GoogleOAuth2Adapter):
    def complete_login(self, request, app, token, **kwargs):
        data = super().complete_login(request, app, token, **kwargs)
        return data


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleAuthAdapter
    serializer_class = GoogleLoginSerializer
    callback_url = "http://localhost:8000/accounts/google/login/callback/"
    client_class = OAuth2Client


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