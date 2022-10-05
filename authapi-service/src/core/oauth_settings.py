from enum import Enum
from core.config import get_settings_instance
import requests
from flask import url_for
from src.api.v1.oauth.extentions import oauth
from src.core.oauth_service import register_social_account


OAUTH_CREDENTIALS: dict[str, dict[str, str]] = {
    "yandex": {
        "id": get_settings_instance().YANDEX_ID,
        "secret": get_settings_instance().YANDEX_SECRET
    },

}


class OAUTH_SERVICES(Enum):
    mail: str = "mail"
    yandex: str = "yandex"


class OAuthSignIn(object):
    providers = None

    def __init__(self, provider_name: str):
        self.provider_name: str = provider_name.value
        credentials: dict[str, str] = OAUTH_CREDENTIALS.get(provider_name.value)
        self.client_id: str = credentials.get("id")
        self.client_secret: str = credentials.get("secret")
        self.service = None

    def get_redirect_url(self) -> str:
        redirect_uri: str = url_for(
            "oauth.auth_provider",
            _external=True, provider=self.provider_name
        )
        return self.service.authorize_redirect(redirect_uri=redirect_uri)

    def get_profile_data(self, request=None):
        pass

    @classmethod
    def get_provider(cls, provider_name: str):
        if not cls.providers:
            cls.providers: dict[str, object] = {}
            for provider_class in cls.__subclasses__():
                provider = provider_class()
                cls.providers[provider.provider_name] = provider
        return cls.providers.get(provider_name)


class YandexSignIn(OAuthSignIn):
    def __init__(self):
        super(YandexSignIn, self).__init__(provider_name=OAUTH_SERVICES.yandex)
        self.service = oauth.register(
            name=self.provider_name,
            client_id=self.client_id,
            client_secret=self.client_secret,
            authorize_url=get_settings_instance().YANDEX_AUTHORIZE_URL,
            response_type="code",
            display="popup",
            scope="login:info login:email",
        )
        print(self.service)

    def get_profile_data(self, request=None):
        code: str = request.args.get("code")
        yandex_response = requests.post(
            url=get_settings_instance().YANDEX_TOKEN_URL,
            data={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "code": code,
                "grant_type": "authorization_code",
            },
        ).json()
        access_token: str = yandex_response.get("access_token")
        user_info_response = requests.get(
            url=get_settings_instance().YANDEX_PROFILE_URL,
            params={
                "format": "json",
                "with_openid_identity": 1,
                "oauth_token": access_token,
            },
        ).json()
        social_id: str = user_info_response.get("id")
        email: str = user_info_response.get("default_email")
        username: str = user_info_response.get("login")
        return register_social_account(
            request=request,
            social_name=self.provider_name,
            social_id=social_id,
            email=email,
            username=username,
        )
