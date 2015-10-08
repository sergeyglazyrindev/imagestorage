import boto3

from .adapters import get_adapter_for_webengine


def get_s3_bucket(bucket, **kwargs):
    session = boto3.session.Session(**kwargs)
    s3 = session.resource('s3')

    def wrapper(s3_key):
        return s3.Object(bucket, s3_key)
    return wrapper


_REGISTERED_BROKERS = {
    'webengine': get_adapter_for_webengine,
    's3': get_s3_bucket
}


class ResourceBroker(object):

    def __init__(self):
        self.resources = {}

    def register(self, alias, value, *args, **kwargs):
        if alias in _REGISTERED_BROKERS:
            self.resources[alias] = _REGISTERED_BROKERS[alias](value, *args, **kwargs)
        else:
            self.resources[alias] = value

    def __getitem__(self, resource):
        return self.resources[resource]

resource_broker = ResourceBroker()
