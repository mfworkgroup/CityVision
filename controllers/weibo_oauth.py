"""
Connects to sina weibo API.
"""
from urlparse import urljoin
from urllib import urlencode
from logging import getLogger

from controllers.common.request_service import CommonRequestService


LOGGER = getLogger(__name__)


class WeiboOauthClient(CommonRequestService):

    def __init__(self, client_id=None, client_secret=None, redirect_url=None):
        self._client_id = client_id
        self._client_secret = client_secret

        self._base_url = 'https://api.weibo.com/'
        self._redirect_url = redirect_url

    def init_app(self, app):

        self._client_id = app.config['WEIBO_CLIENT_ID']
        self._client_secret = app.config['WEIBO_CLIENT_SECRET']
        self._redirect_url = app.config['WEIBO_REDIRECT_URL']

    @property
    def base_url(self):
        return self._base_url

    @property
    def redirect_url(self):
        return self._redirect_url

    def get_oauth_url(self, redirect_url=None, response_type='code'):
        if redirect_url is None:
            redirect_url = self.redirect_url
        request_endpoint = 'oauth2/authorize'

        request_base_url = urljoin(self.base_url, request_endpoint)
        query_string = urlencode({'client_id': self._client_id, 'redirect_uri': redirect_url,
                                  'response_type': response_type})
        request_url = '{}?{}'.format(request_base_url, query_string)
        return request_url

    def get_access_token(self, authorization_code, redirect_url=None):
        if redirect_url is not None:
            redirect_url = self.redirect_url
        request_endpoint = 'oauth2/access_token'
        request_base_url = urljoin(self.base_url, request_endpoint)
        payload = {'client_id': self._client_id, 'client_secret': self._client_secret,
                   'grand_type': 'authorization_code', 'code': authorization_code, 'redirect_url': redirect_url}

        response_payload = super(WeiboOauthClient, self).json_request(request_url=request_base_url, method='POST',
                                                                      json=payload)
        # TODO error handling
        access_token = response_payload['access_token']
        LOGGER.info('access_token={} for authorization_code={}: {}'.format(access_token, authorization_code,
                                                                           response_payload))
        return access_token
