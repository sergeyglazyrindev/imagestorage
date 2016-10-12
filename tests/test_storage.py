import os
import mock
from unittest import TestCase

from PIL import Image
from awsstorage import storage
from awsstorage.resources_broker import resource_broker
from awsstorage.data_models import AwsFileToUpload


class BaseImageStorageTestCase(TestCase):

    def setUp(self):
        self.bucket = storage.Bucket(
            'https://s3.eu-central-1.amazonaws.com/testimagestorageforpippackage/'
        )
        resource_broker.register(
            's3', 'testimagestorage', aws_access_key_id='dsadasd',
            aws_secret_access_key='dsasda', region_name='eu-central-1'
        )


class TestImageStorage(BaseImageStorageTestCase):

    @mock.patch('awsstorage.base.requests')
    @mock.patch('awsstorage.adapters.wheezy.wheezy.http')
    @mock.patch('awsstorage.storage.s3_store_image')
    def test(self, mocked_task, patched_wheezy, *args):
        mocked_task.return_value = mock.MagicMock()
        storage_ = storage.S3ImageStorage(101, 'jpg')
        storage_.use_bucket(self.bucket)
        memcache_mocked = mock.MagicMock()
        resource_broker.register('cache_service', memcache_mocked)
        resource_broker.register('webengine', 'wheezy')
        image = Image.open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'test.jpg')))
        with mock.patch.object(storage_, '_get_image_from_url') as mocked_object:
            memcache_mocked.get.return_value = False
            mocked_object.return_value = image
            storage_.store_origin_from_file(
                image,
                '4000x4000'
            )
            mock_to_compare = mock.MagicMock()
            patched_wheezy.HTTPResponse.return_value = mock_to_compare
            storage_.get_requested_image('https://microsoft.com/?size=200x100')
            patched_wheezy.HTTPResponse.assert_called_with(content_type='image/jpeg')
            mock_to_compare.write_bytes.assert_called_with(image.tobytes())
            storage_.get_requested_image((200, 100))


class TestFileStorage(BaseImageStorageTestCase):

    @mock.patch('awsstorage.storage.s3_store_file')
    def test(self, *args):
        storage_ = storage.S3FileStorage()
        storage_.use_bucket(self.bucket)
        file_ = AwsFileToUpload(
            os.path.join(os.path.dirname(__file__), 'test.jpg'),
            'test.jpg', 1
        )
        self.assertTrue(storage_.store(
            file_,
        ).endswith('test.jpg'))
