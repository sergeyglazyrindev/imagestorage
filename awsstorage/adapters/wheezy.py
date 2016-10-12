import wheezy.http

from .helpers import get_mimetype_for_pilimage


class HttpEngineAdapter(object):

    @classmethod
    def permanent_redirect(cls, url):
        return wheezy.http.permanent_redirect(url)

    @classmethod
    def image_response(cls, pil_image):
        response = wheezy.http.HTTPResponse(content_type=get_mimetype_for_pilimage(pil_image.format))
        response.write_bytes(pil_image.tobytes())
        return response
