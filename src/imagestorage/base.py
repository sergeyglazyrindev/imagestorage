import memcache
from urllib.parse import urlparse, parse_qs
from PIL import Image
import io
import requests

from .adapters import get_adapter_for_webengine
from .helpers import size_string_to_tuple
from .exceptions import ImageNotFound
from .decorators import cached_property


class BaseStorage():

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

    def store_origin(self, image_url, origin_size):
        raise NotImplementedError

    def configure_webengine(self, webengine):
        self._webengine = webengine

    @cached_property
    def webengine(self):
        return get_adapter_for_webengine(self._webengine)

    def _resize_image(self, pil_image, size_tuple):
        if isinstance(size_tuple, str):
            size_tuple = size_string_to_tuple(size_tuple)
        pil_image.thumbnail(size_tuple)

    def configure_memcache(self, hosts):
        self.mc = memcache.Client(hosts, debug=0)
