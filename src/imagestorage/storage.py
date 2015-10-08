import requests
from urllib.parse import urlunparse, urlparse

from .base import BaseStorage
from .tasks import s3_store_image
from .exceptions import ImageStoreOriginError
from .resources_broker import resource_broker


class S3ImageStorage(BaseStorage):

    image_id = None
    base_path = None
    is_configured = False
    domain = None
    image_ext = None
    bucket_base_path = None

    def store_origin(self, image_url, origin_size):
        if not self.is_configured:
            return
        pil_image = self._get_image_from_url(image_url)
        self._resize_image(pil_image, origin_size)
        success = s3_store_image.apply_async(args=(
            pil_image, self.__get_image_key('origin'))
        ).wait(timeout=10, interval=0.1)
        if not success:
            raise ImageStoreOriginError('Error while storing origin image')
        return self.__image_url('origin')

    def get_requested_image(self, image_url_or_tuple):
        if not self.is_configured:
            return
        if isinstance(image_url_or_tuple, (tuple, list)):
            size_tuple = image_url_or_tuple
        else:
            size_tuple = self._get_size_tuple_from_image_url(image_url_or_tuple)
        requesting_image_url = self.__image_url(size_tuple)
        image_key = self.__get_image_key(size_tuple)
        avail_image_key = image_key + '_avail'
        cache_service = resource_broker['cache_service']
        is_available_image = cache_service.get(avail_image_key)
        if is_available_image or self._image_is_available(requesting_image_url):
            if not is_available_image:
                cache_service.set(avail_image_key, 1)
            return resource_broker['webengine'].permanent_redirect(requesting_image_url)
        pil_image = self._get_image_from_url(self.__image_url('origin'))
        self._resize_image(pil_image, size_tuple)
        if cache_service.add(image_key, 1, time=60):
            s3_store_image.delay(pil_image, image_key)
        return resource_broker['webengine'].image_response(pil_image)

    def _image_is_available(self, image_url):
        return bool(requests.head(image_url).status_code == 200)

    def __image_url(self, size_tuple):
        s3_parts = self.s3_parts
        return urlunparse((
            s3_parts.scheme,
            s3_parts.netloc,
            s3_parts.path + self.__get_image_key(size_tuple),
            '',
            '',
            ''
        ))

    def __get_image_key(self, size_tuple):
        if size_tuple == 'origin':
            size_tuple_part = size_tuple
        else:
            size_tuple = map(str, filter(None, size_tuple))
            size_tuple_part = 'x'.join(size_tuple)
        return str(self.image_id) + '/' + size_tuple_part + '.' + self.image_ext

    @property
    def s3_parts(self):
        return urlparse(self.bucket_base_path)

    def configure(self, bucket_base_path, base_path='/'):
        self.base_path = base_path
        self.bucket_base_path = bucket_base_path
        self.is_configured = True
