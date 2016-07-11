from django.shortcuts import redirect
from django.http import HttpResponse


from .helpers import get_mimetype_for_pilimage


class HttpEngineAdapter(object):

    @classmethod
    def permanent_redirect(cls, url):
        return redirect(url, permanent=True)

    @classmethod
    def image_response(cls, pil_image):
        response = HttpResponse(
            content_type=get_mimetype_for_pilimage(pil_image.format)
        )
        pil_image.save(response, pil_image.format)
        return response
