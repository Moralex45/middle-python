from flask import request, Blueprint
from src.core.oauth_settings import OAuthSignIn

blueprint = Blueprint("oauth", __name__, url_prefix="/api/v1/oauth")


@blueprint.route("/login/<provider>", methods=['POST'])
def login_provider(provider: str):

    provider_oauth = OAuthSignIn.get_provider(provider_name=provider)
    return provider_oauth.get_redirect_url()


@blueprint.route("/auth/<provider>", methods=['GET'])
def auth_provider(provider: str):

    provider_oauth = OAuthSignIn.get_provider(provider_name=provider)
    return provider_oauth.get_profile_data(request=request)
