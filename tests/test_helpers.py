from unittest import TestCase

from src.imagestorage.helpers import size_string_to_tuple


class TestHelper(TestCase):

    def test(self):

        self.assertEqual(size_string_to_tuple('200x200'), (200, 200))
        with self.assertRaises(ValueError):
            size_string_to_tuple('sasx200'), (200, 200)
