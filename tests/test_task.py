import os
import mock
from unittest import TestCase

from src.imagestorage.tasks import s3_store_image
from PIL import Image


class TestTask(TestCase):

    @mock.patch('src.imagestorage.tasks.boto3.session.Session.resource', autospec=True)
    def test(self, patched_boto3):

        tmp_mock = mock.MagicMock()
        mock_to_compare = mock.MagicMock()
        tmp_mock.Object.return_value = mock_to_compare
        patched_boto3.return_value = tmp_mock
        image = Image.open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'test.jpg')))
        res = s3_store_image(image, {'access_key': '', 'secret_key': ''}, '', '/')
        self.assertTrue(mock_to_compare.get.called)
        self.assertTrue(res is None)
        mock_to_compare.get.return_value = False
        res = s3_store_image(image, {'access_key': '', 'secret_key': ''}, '', '/')
        self.assertTrue(mock_to_compare.upload_file.called)
