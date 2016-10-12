import os
import mock
from unittest import TestCase

from awsstorage.tasks import s3_store_image, s3_store_file
from awsstorage.resources_broker import resource_broker
from PIL import Image


class TestTask(TestCase):

    def setUp(self):
        self.mock_to_compare = mock.MagicMock()
        s3_mock = mock.MagicMock(return_value=self.mock_to_compare)
        self.old_s3_handler = resource_broker.resources.get('s3')
        resource_broker.resources['s3'] = s3_mock

    def tearDown(self):
        resource_broker.resources['s3'] = self.old_s3_handler

    def test_image(self):

        self.mock_to_compare.get.return_value = True
        image = Image.open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'test.jpg')))
        s3_store_image(image, '/dsadsa.jpg')
        self.assertTrue(self.mock_to_compare.upload_file.called)

    def test_file(self):

        s3_store_file(os.path.join(os.path.dirname(__file__), 'test.jpg'), 'dasdas')
        self.assertTrue(self.mock_to_compare.upload_file.called)
