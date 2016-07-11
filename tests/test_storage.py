import os
import mock
from unittest import TestCase

from PIL import Image
from src.imagestorage import storage as imagestorage
from src.imagestorage.resources_broker import resource_broker


class TestTask(TestCase):

    @mock.patch('src.imagestorage.base.requests')
    @mock.patch('src.imagestorage.adapters.wheezy.wheezy.http')
    @mock.patch('src.imagestorage.storage.s3_store_image')
    def test(self, mocked_task, patched_wheezy, *args):
        mocked_task.return_value = mock.MagicMock()
        storage = imagestorage.S3ImageStorage(101, 'jpg')
        resource_broker.register('s3', 'testimagestorage', aws_access_key_id='dsadasd', aws_secret_access_key='dsasda',
                                 region_name='eu-central-1')
        memcache_mocked = mock.MagicMock()
        resource_broker.register('cache_service', memcache_mocked)
        resource_broker.register('webengine', 'wheezy')
        storage.configure(
            'https://s3.eu-central-1.amazonaws.com/testimagestorageforpippackage/',
            '/',
        )
        image = Image.open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'test.jpg')))
        with mock.patch.object(storage, '_get_image_from_url') as mocked_object:
            memcache_mocked.get.return_value = False
            mocked_object.return_value = image
            storage.store_origin_from_file(
                image,
                '4000x4000'
            )
            mock_to_compare = mock.MagicMock()
            patched_wheezy.HTTPResponse.return_value = mock_to_compare
            storage.get_requested_image('https://microsoft.com/?size=200x100')
            patched_wheezy.HTTPResponse.assert_called_with(content_type='image/jpeg')
            mock_to_compare.write_bytes.assert_called_with(image.tobytes())
            storage.get_requested_image((200, 100))
