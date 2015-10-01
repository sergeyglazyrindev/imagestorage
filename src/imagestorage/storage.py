import requests
from urllib.parse import urlunparse, urlparse

from .interfaces import IStorage
from .tasks import s3_store_image
from .exceptions import ImageStoreOriginError


class S3ImageStorage(object):

    image_id = None
    tokens = None
    bucket = None
    base_path = None
    is_configured = False
    domain = None
    image_ext = None

    def __init__(self, image_id, image_ext):
        self.image_id = image_id
        self.image_ext = image_ext

    def store_origin(self, image_url, origin_size):
        if not self.is_configured:
            return
        pil_image = self._get_image_from_url(image_url)
        self._resize_image(pil_image, origin_size)
        success = s3_store_image.apply_async(args=(
            pil_image, self.tokens, self.bucket, 'origin', self.__get_image_key(origin_size, format='origin'))
        ).wait(timeout=None, interval=0.1)
        if not success:
            raise ImageStoreOriginError('Error while storing origin image')
        return self.__image_url(origin_size)

    def get_requested_image(self, image_url):
        if not self.is_configured:
            return
        size_tuple = self._get_size_tuple_from_image_url(image_url)
        requesting_image_url = self.__image_url(size_tuple)
        if self._image_is_available(requesting_image_url):
            return self.webengine.permanent_redirect(requesting_image_url)
        pil_image = self._get_image_from_url(self.__image_url('origin'))
        self._resize_image(pil_image, size_tuple)
        size_tuple_string = 'x'.join(size_tuple)
        image_key = self.__get_image_key(size_tuple, format=size_tuple_string)
        if self.mc.add(image_key, 1, time=60):
            s3_store_image.delay(pil_image, self.tokens, self.bucket, size_tuple_string, image_key)
        return self.webengine.image_response(pil_image)

    def _image_is_available(self, image_url):
        return bool(requests.head(image_url).status_code == 200)

    def __image_url(self, size_tuple):
        return urlunparse((
            self.s3_parts.scheme,
            self.s3_parts.netloc,
            self.__get_image_key(size_tuple)
        ))

    def __get_image_key(self, size_tuple, format=None):
        size_tuple = map(str, filter(None, size_tuple))
        if format == 'origin':
            size_tuple_part = format
        else:
            size_tuple_part = 'x'.join(size_tuple)
        return self.s3_parts.path + '/' + str(self.image_id) + '/' + size_tuple_part + '.' + self.image_ext

    @property
    def s3_parts(self):
        return urlparse(self.base_path)

    def configure(self, tokens, bucket, base_path):
        self.tokens = tokens
        self.bucket = bucket
        self.base_path = base_path
        self.is_configured = True

IStorage.register(S3ImageStorage)
