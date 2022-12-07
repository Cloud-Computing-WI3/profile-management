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
from accounts.serializers import GoogleLoginSerializer, AccountSerializer, RegistrationSerializer
from django.dispatch import receiver
from allauth.socialaccount.signals import social_account_updated
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
import urllib.request
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from categories.serializers import CategorySerializer


class RegistrationViewSet(ModelViewSet, TokenObtainPairView):
    serializer_class = RegistrationSerializer
    permission_classes = (AllowAny,)
    http_method_names = ["post"]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        res = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

        return Response({
            "user": serializer.data,
            "refresh": res["refresh"],
            "token": res["access"]
        }, status=status.HTTP_201_CREATED)


class AccountView(ModelViewSet):
    serializer_class = AccountSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Account.objects.all()
    http_method_names = ["get", "put", "patch", "head", "options", "trace", "delete", ]

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

    def update(self, request, pk=None):
        queryset = Account.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = AccountSerializer(user, data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


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
        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(urllib.request.urlopen(picture_url).read())
        img_temp.flush()
        user.picture = File(img_temp)
    user.given_name = given_name
    user.family_name = family_name
    user.save()
@api_view(["GET", "POST", "PUT"])
def get_user_categories(request, pk=None):
    if request.method == "GET":
        account = Account.objects.get(pk=pk)
        serializer = CategorySerializer(account.categories.all(), many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)