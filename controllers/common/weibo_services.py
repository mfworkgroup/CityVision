"""
Talks to weibo POI service
"""
from enum import Enum
import random
import urllib
import urlparse
from logging import getLogger


from controllers.common.request_service import CommonRequestService

LOGGER = getLogger(__name__)


class WeiboCommonServiceState(Enum):
    single = 0
    batch = 1


class WeiboCommonService(CommonRequestService):
    def __init__(self, access_tokens, mode=WeiboCommonServiceState.batch):
        self._access_tokens = set(access_tokens)
        if isinstance(mode, WeiboBatchUserService):
            raise ValueError('Invalid service mode')
        self._mode = mode

        self._base_url = 'https://api.weibo.com/2/'

    @property
    def mode(self):
        return self._mode

    @property
    def access_tokens(self):
        return self._access_tokens

    @property
    def base_url(self):
        return self._base_url

    def get_access_token(self):
        raise NotImplementedError()

    def add_access_token(self, access_token):
        raise NotImplementedError()

    def request(self, partial_url, method, url_parameters=None, json=None):
        if url_parameters is None:
            url_parameters['access_token'] = self.get_access_token()
        request_url = urlparse.urljoin(self.base_url, partial_url) + '?' + urllib.urlencode(url_parameters)

        return super(WeiboCommonService, self).json_request(request_url=request_url, method=method, json=json)


class WeiboSingleUserService(WeiboCommonService):

    def __init__(self, access_token):
        self._access_token = access_token
        super(WeiboSingleUserService, self).__init__(access_tokens={access_token}, mode=WeiboCommonServiceState.single)

    def get_access_token(self):
        return self._access_token

    def add_access_token(self, access_token):
        if self._access_token is None:
            self._access_token = access_token
        else:
            raise ValueError('Client already has an access token')


class WeiboBatchUserService(WeiboCommonService):

    def __init__(self, access_tokens):
        if isinstance(access_tokens, (list, set)):
            super(WeiboBatchUserService, self).__init__(access_tokens=access_tokens)
        elif isinstance(access_tokens, str):
            super(WeiboBatchUserService, self).__init__(access_tokens={access_tokens})
        else:
            raise TypeError('access_tokens must be a list, str or set')

    def get_access_token(self):
        return random.choice(self.access_tokens)

    def add_access_token(self, access_token):
        LOGGER.info('Adding access_token={} to a set of {}'.format(access_token, len(self.access_tokens)))
        self.access_tokens.add(access_token)

    def add_access_tokens(self, access_tokens):
        self._access_tokens = self.access_tokens.union(access_tokens)
