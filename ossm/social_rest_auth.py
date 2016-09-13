from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
from rest_framework.authentication import TokenAuthentication


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
    authentication_classes = (TokenAuthentication, )


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    authentication_classes = (TokenAuthentication, )


class GitHubLogin(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter
    authentication_classes = (TokenAuthentication, )
