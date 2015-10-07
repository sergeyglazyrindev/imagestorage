import os
import mock
from unittest import TestCase

from PIL import Image
from src.imagestorage.adapters import get_adapter_for_webengine


class TestTask(TestCase):

    def setUp(self):
        fp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'test.jpg'))
        self.image = Image.open(fp)

    @mock.patch('src.imagestorage.adapters.wheezy.wheezy.http')
    def test_wheezy(self, patched_wheezy):

        webengine = get_adapter_for_webengine('wheezy')
        webengine.permanent_redirect('http://microsoft.com')
        self.assertTrue(patched_wheezy.permanent_redirect.called)
        patched_wheezy.permanent_redirect.assert_called_with('http://microsoft.com')
        mock_to_compare = mock.MagicMock()
        patched_wheezy.HTTPResponse.return_value = mock_to_compare
        webengine.image_response(self.image)
        patched_wheezy.HTTPResponse.assert_called_with(content_type='image/jpeg')
        mock_to_compare.write_bytes.assert_called_with(self.image.tobytes())
