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
from rest_framework.decorators import api_view, permission_classes
from categories.serializers import CategorySerializer
from keywords.serializers import KeywordSerializer

class RegistrationViewSet(ModelViewSet, TokenObtainPairView):
    # specify the serializer class to be used
    serializer_class = RegistrationSerializer
    # specify the permission classes, in this case, it allows any user to make a request
    permission_classes = (AllowAny,)
    # specify the allowed http methods, in this case only "post" is allowed
    http_method_names = ["post"]

    def create(self, request, *args, **kwargs):
        # get the serializer instance using the request data
        serializer = self.get_serializer(data=request.data)

        # validate the serializer
        serializer.is_valid(raise_exception=True)
        #save the user
        user = serializer.save()
        #create a refresh token for the user
        refresh = RefreshToken.for_user(user)
        res = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

        #return the response including the user data, refresh token and access token
        return Response({
            "user": serializer.data,
            "refresh": res["refresh"],
            "token": res["access"]
        }, status=status.HTTP_201_CREATED)



class AccountView(ModelViewSet):
    # specify the serializer class to be used
    serializer_class = AccountSerializer
    # specify the permission classes, in this case, only authenticated users can make requests
    permission_classes = (IsAuthenticated,)
    # specify the queryset to be used for listing and retrieving objects
    queryset = Account.objects.all()
    # specify the allowed http methods
    http_method_names = ["get", "put", "patch", "head", "options", "trace", "delete", ]

    def retrieve(self, request, pk=None):
        # retrieve the user object with the given pk
        queryset = Account.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        # create a serializer instance using the user object
        serializer = AccountSerializer(user)
        # return the serialized user data
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        # retrieve all user objects
        profiles = Account.objects.all()
        # create a serializer instance using the user objects
        serializer = AccountSerializer(profiles, many=True)
        # return the serialized user data
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        pass

    def update(self, request, pk=None):
        # retrieve the user object with the given pk
        queryset = Account.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        # create a serializer instance using the user object and the request data
        serializer = AccountSerializer(user, data=request.data)

        if serializer.is_valid(raise_exception=True):
            # save the changes and return the serialized user data
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
    # get the user associated with the social account
    user = sociallogin.user
    # check if the social account provider is not None
    if sociallogin.account.provider is not None:
        # retrieve the extra data associated with the social account
        user_data = sociallogin.account.extra_data
        # retrieve the picture url from the extra data
        picture_url = user_data["picture"]
        # retrieve the given name and family name from the extra data
        given_name = user_data["given_name"]
        family_name = user_data["family_name"]
        # create a temporary file to store the picture
        img_temp = NamedTemporaryFile(delete=True)
        # download the picture and save it to the temporary file
        img_temp.write(urllib.request.urlopen(picture_url).read())
        img_temp.flush()
        # set the user's picture to the temporary file
        user.picture = File(img_temp)
    # set the user's given name and family name
    user.given_name = given_name
    user.family_name = family_name
    # save the changes to the user
    user.save()



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_categories(request):
    if request.method == "GET":
        account = Account.objects.get(pk=request.user.pk)
        serializer = CategorySerializer(account.categories.all(), many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_keywords(request):
    if request.method == "GET":
        account = Account.objects.get(pk=request.user.pk)
        serializer = KeywordSerializer(account.keywords.all(), many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)