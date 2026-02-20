import unittest

from gencontent import extract_title

class TestMain(unittest.TestCase):
    def test_extract_title(self):
        md = "# This is a heading 1"
        title = extract_title(md)
        self.assertEqual(title, "This is a heading 1")

    def test_extract_title_just_heading(self):
        md = """
# This is the heading

But this is not.
        """
        title = extract_title(md)

        self.assertEqual(title, "This is the heading")

    def test_extract_title_not_heading1(self):
        md = "## This is not a heading 1"
        with self.assertRaises(Exception):
            extract_title(md)

    def test_extract_title_not_a_heading(self):
        md = "This is not even a heading"
        with self.assertRaises(Exception):
            extract_title(md)

