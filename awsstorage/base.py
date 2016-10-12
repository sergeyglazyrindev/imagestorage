from urllib.parse import urlparse, parse_qs
from PIL import Image
import io
import requests

from .helpers import size_string_to_tuple
from .exceptions import ImageNotFound
from .resources_broker import ResourceResolver


class BaseStorage():

    mc = ResourceResolver('cache_service')
    webengine = ResourceResolver('webengine')


class BaseImageStorage(BaseStorage):

    def __init__(self, image_id, image_ext):
        self.image_id = image_id
        self.image_ext = image_ext

    def get_requested_image(self, image_url):
        raise NotImplementedError

    def _get_size_tuple_from_image_url(self, image_url):
        url_parts = urlparse(image_url)
        size_tuple = size_string_to_tuple(parse_qs(url_parts.query)['size'].pop())
        return size_tuple

    def _get_image_from_url(self, image_url):
        image_string = requests.get(image_url).content
        if not image_string:
            raise ImageNotFound('Couldn\'t download image from {}'.format(image_url))
        return Image.open(io.BytesIO(image_string))

    def store_origin_from_url(self, image_url, origin_size):
        raise NotImplementedError

    def store_origin_from_file(self, pil_image, origin_size):
        raise NotImplementedError

    def _resize_image(self, pil_image, size_tuple):
        if isinstance(size_tuple, str):
            size_tuple = size_string_to_tuple(size_tuple)
        pil_image.thumbnail(size_tuple)
