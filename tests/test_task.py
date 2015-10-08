import os
import mock
from unittest import TestCase

from src.imagestorage.tasks import s3_store_image
from src.imagestorage.resources_broker import resource_broker
from PIL import Image


class TestTask(TestCase):

    def test(self):

        mock_to_compare = mock.MagicMock()
        s3_mock = mock.MagicMock(return_value=mock_to_compare)
        resource_broker.resources['s3'] = s3_mock
        mock_to_compare.get.return_value = True
        image = Image.open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'test.jpg')))
        res = s3_store_image(image, '/dsadsa.jpg')
        self.assertTrue(mock_to_compare.get.called)
        self.assertTrue(res is None)
        mock_to_compare.get.return_value = False
        res = s3_store_image(image, '/sasa.jpg')
        self.assertTrue(mock_to_compare.upload_file.called)
