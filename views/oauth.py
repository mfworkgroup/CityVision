from flask import Blueprint, request, redirect

from logging import getLogger

from extensions import oauth_service, weibo_client


LOGGER = getLogger(__name__)
oauth_blueprint = Blueprint('oauth', __name__)


@oauth_blueprint.route('/authorize/')
def redirect_to_authorization():
    oauth_url = oauth_service.get_oauth_url()
    LOGGER.info('redirect to oauth_url={}'.format(oauth_url))
    return redirect(oauth_url)


@oauth_blueprint.route('/register_token/')
def get_access_token():
    authorization_code = request.args.get('code')
    LOGGER.info('registering access token with code={}'.format(authorization_code))

    access_token = oauth_service.get_access_token(authorization_code)
    weibo_client.add_access_token(access_token)

    return access_token

