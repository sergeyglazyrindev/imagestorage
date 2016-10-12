import tempfile

from .resources_broker import ResourceResolver


def s3_store_image(pil_image, s3_key):

    if s3_key.startswith('/'):
        s3_key = s3_key[1:]
    _object = ResourceResolver('s3')(s3_key)
    tmp_file = tempfile.NamedTemporaryFile(prefix='imagestorage')
    pil_image.save(tmp_file, pil_image.format)
    tmp_file.seek(0)
    _object.upload_file(tmp_file.name)
    return True


def s3_store_file(file_, s3_key):

    if s3_key.startswith('/'):
        s3_key = s3_key[1:]
    _object = ResourceResolver('s3')(s3_key)
    _object.upload_file(file_)
    return True
