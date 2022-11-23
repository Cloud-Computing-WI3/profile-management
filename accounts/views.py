from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from accounts.serializers import LoginSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework.response import Response
from rest_framework import status
from accounts.models import Account
from accounts.serializers import GoogleLoginSerializer, AccountSerializer
from django.dispatch import receiver
from allauth.socialaccount.signals import social_account_updated
import urllib.request
from django.core.files import File

class AccountView(ModelViewSet):
    serializer_class = AccountSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Account.objects.all()
    http_method_names = ["get", "post", "put", "delete"]

    def retrieve(self, request, pk=None):
        queryset = Account.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = AccountSerializer(user)
        return Response(serializer.data)


    def list(self, request, *args, **kwargs):
        profiles = Account.objects.all()
        serializer = AccountSerializer(profiles, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        pass

    def update(self, request, *args, **kwargs):
        pass

    def destroy(self, request, *args, **kwargs):
        pass
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


@receiver(social_account_updated)
def populate_profile(sociallogin, **kwargs):
    user = sociallogin.user
    if sociallogin.account.provider is not None:
        user_data = sociallogin.account.extra_data
        picture_url = user_data["picture"]
        given_name = user_data["given_name"]
        family_name = user_data["family_name"]

    #TODO: Upload image to file storage
    user.given_name = given_name
    user.family_name = family_name
    user.save()
