import boto


def s3_store_image(pil_image, tokens, bucket, format, s3_key):

    conn = boto.s3.connection.S3Connection(tokens['access_key'], tokens['secret_key'])
    b = conn.get_bucket(bucket)
    key = b.get_key(s3_key)
    if not key:
        return
    success = bool(key.set_contents_from_string(pil_image.tobytes()))
    return success
