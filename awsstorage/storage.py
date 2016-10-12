import os
import string
import requests
from urllib.parse import urlunparse, urlparse

from .base import BaseStorage, BaseImageStorage
from .tasks import s3_store_image, s3_store_file
from .exceptions import ImageStoreOriginError, FileStoreError
import random


class Bucket(object):

    __slots__ = ('bucket_base_path', 'base_path')

    def __init__(self, bucket_base_path, base_path='/'):
        self.bucket_base_path = bucket_base_path
        self.base_path = base_path


class S3ImageStorage(BaseImageStorage):

    image_id = None
    domain = None
    image_ext = None
    bucket = None

    def store_origin_from_url(self, image_url, origin_size):
        pil_image = self._get_image_from_url(image_url)
        return self._store_origin(pil_image, origin_size)

    def _store_origin(self, pil_image, origin_size):
        self._resize_image(pil_image, origin_size)
        success = s3_store_image.apply_async(args=(
            pil_image, self.__get_image_key('origin'))
        ).wait(timeout=10, interval=0.1)
        if not success:
            raise ImageStoreOriginError('Error while storing origin image')
        return self._image_url('origin')

    def store_origin_from_file(self, pil_image, origin_size):
        return self._store_origin(pil_image, origin_size)

    def get_requested_image(self, image_url_or_tuple, return_image=False):
        if isinstance(image_url_or_tuple, (tuple, list)):
            size_tuple = image_url_or_tuple
        else:
            size_tuple = self._get_size_tuple_from_image_url(image_url_or_tuple)
        requesting_image_url = self._image_url(size_tuple)
        image_key = self.__get_image_key(size_tuple)
        avail_image_key = image_key + '_avail'
        cache_service = self.mc
        is_available_image = cache_service.get(avail_image_key)
        if not return_image and (is_available_image or self._image_is_available(requesting_image_url)):
            if not is_available_image:
                cache_service.set(avail_image_key, 1)
            return self.webengine.permanent_redirect(requesting_image_url)
        pil_image = self._get_image_from_url(self._image_url('origin'))
        self._resize_image(pil_image, size_tuple)
        if cache_service.add(image_key, 1, time=60):
            s3_store_image.delay(pil_image, image_key)
        return self.webengine.image_response(pil_image)

    def _image_is_available(self, image_url):
        return bool(requests.head(image_url).status_code == 200)

    def _image_url(self, size_tuple):
        s3_parts = self.s3_parts
        path = s3_parts.path
        return urlunparse((
            s3_parts.scheme,
            s3_parts.netloc,
            path + self.__get_image_key(size_tuple),
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
        return self.bucket.base_path + str(self.image_id) + '/' + size_tuple_part + '.' + self.image_ext

    @property
    def s3_parts(self):
        return urlparse(self.bucket.bucket_base_path)

    @classmethod
    def use_bucket(cls, bucket):
        cls.bucket = bucket


class S3FileStorage(BaseStorage):

    bucket = None

    def store(self, filepath):
        storage_key = self._get_storage_key(filepath)
        success = s3_store_file.apply_async(args=(
            filepath, storage_key
        )).wait(timeout=10, interval=0.1)
        if not success:
            raise FileStoreError('Error while storing file')
        return self._file_url(storage_key)

    def _get_storage_key(self, filepath):
        random_part = ''.join(random.SystemRandom().choice(
            string.ascii_uppercase + string.digits
        ) for _ in range(20))
        file_parts = (
            random_part[:3],
            random_part[4:6],
            random_part[7:9],
            random_part,
            os.path.basename(filepath)
        )
        return '/'.join(file_parts)

    def _file_url(self, storage_key):
        s3_parts = self.s3_parts
        path = s3_parts.path
        return urlunparse((
            s3_parts.scheme,
            s3_parts.netloc,
            path + storage_key,
            '',
            '',
            ''
        ))

    @property
    def s3_parts(self):
        return urlparse(self.bucket.bucket_base_path)

    @classmethod
    def use_bucket(cls, bucket):
        cls.bucket = bucket
