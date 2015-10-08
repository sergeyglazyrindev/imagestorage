import botocore
import tempfile

from .resources_broker import resource_broker


def s3_store_image(pil_image, s3_key):

    if s3_key.startswith('/'):
        s3_key = s3_key[1:]
    _object = resource_broker['s3'](s3_key)
    try:
        if _object.get():
            return
    except botocore.exceptions.ClientError:
        pass
    tmp_file = tempfile.NamedTemporaryFile(prefix='imagestorage')
    pil_image.save(tmp_file, pil_image.format)
    tmp_file.seek(0)
    _object.upload_file(tmp_file.name)
    return True
