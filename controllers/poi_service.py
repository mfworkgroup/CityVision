from urlparse import urljoin
from urllib import urlencode
from logging import getLogger

from requests.exceptions import HTTPError


LOGGER = getLogger(__name__)


class POIService(object):

    def __init__(self, weibo_client=None):
        self._weibo_client = weibo_client
        self._base_url = 'place/'

    @property
    def client(self):
        return self._weibo_client

    def search_for_poi(self, keyword, city=None, category=None, page=None, count=None):
        """
        Search for poi according to keyword
        :param keyword: search keyword
        :param city: search in city; if not provided it will search within china
        :param category: poi category
        :param page: page; by default it will be 1
        :param count: page size, default is 20, max is 50.
        :return:
        """
        LOGGER.info('Searching for poi\'s with keyword={}, city={}, category={}, page={}, count={}'.format(
            keyword, city, category, page, count))

        method = 'GET'
        poi_url = urljoin(self._base_url, 'pois/search.json')
        url_parameters = {
            'keyword': keyword
        }
        for keyword, value in {'city': city, 'category': category, 'page': page, 'count': count}:
            if value is not None:
                url_parameters[keyword] = value

        try:
            return self.client.request(partial_url=poi_url, method=method, url_parameters=url_parameters)
        except HTTPError:
            # TODO deal with it.
            raise
