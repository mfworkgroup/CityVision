from logging import getLogger
from json import dumps, loads
import os


LOGGER = getLogger(__name__)


class StorageBase(object):
    def write(self, access_tokens):
        raise NotImplementedError()

    def clear(self):
        raise NotImplementedError()

    def remove(self, access_token):
        raise NotImplementedError()

    def load(self):
        raise NotImplementedError()


# TODO use S3 instead
class FileStorage(StorageBase):
    def __init__(self, file_name='access_token.json'):
        self._file_name = file_name

    @property
    def file_name(self):
        return self._file_name

    def write(self, access_tokens):
        LOGGER.info('Writing {} access tokens to disk'.format(len(access_tokens)))

        # set is not json-serializable.
        payload = list(access_tokens)
        with open(self.file_name, 'w') as f:
            f.write(dumps(payload))

    def clear(self):
        os.remove(self.file_name)

    def remove(self, access_token):
        existing_tokens = self.load()

        try:
            existing_tokens.remove(access_token)
        except ValueError:
            return
        LOGGER.info('Removing 1 token access_token={} from storage'.format(access_token))
        self.write(existing_tokens)

    def load(self):
        LOGGER.info('Loading access tokens from file.')

        access_tokens = {}
        try:
            with open(self.file_name) as f:
                payload = f.read()
        except IOError:
            LOGGER.info('No file found for access tokens.')
            return access_tokens

        access_tokens = loads(payload)
        LOGGER.info('Loaded {} access tokens from file'.format(len(access_tokens)))
        return access_tokens
