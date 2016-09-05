from logging import getLogger

import requests


LOGGER = getLogger(__name__)


class CommonRequestService(object):
    """
    Handles http requests.
    """

    # TODO might as well just be a function
    @staticmethod
    def json_request(request_url, method, json=None):
        LOGGER.info('requesting request_url={}, method={}, json={}'.format(request_url, method, json))
        response = requests.request(method=method, url=request_url, json=json)
        response.raise_for_status()
        return response.json()
