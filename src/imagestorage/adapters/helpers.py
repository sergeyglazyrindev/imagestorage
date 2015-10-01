from ..exceptions import ImageFormatNotSupported


def get_mimetype_for_pilimage(pil_image_format):
    image_format_to_mimetype = {
        'gif': 'image/gif',
        'jpeg': 'image/jpeg',
        'png': 'image/png',
    }
    try:
        return image_format_to_mimetype[pil_image_format.lower()]
    except KeyError:
        raise ImageFormatNotSupported('format {} not supported'.format(pil_image_format.lower()))
