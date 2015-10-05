import boto3
import botocore
import tempfile


def s3_store_image(pil_image, tokens, bucket, s3_key):

    session = boto3.session.Session(aws_access_key_id=tokens['access_key'],
                                    aws_secret_access_key=tokens['secret_key'],
                                    region_name='eu-central-1')
    s3 = session.resource('s3')
    if s3_key.startswith('/'):
        s3_key = s3_key[1:]
    _object = s3.Object(bucket, s3_key)
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
