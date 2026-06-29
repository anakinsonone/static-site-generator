import unittest

from markdown_blocks import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_with_whitespace(self):
        self.assertEqual(extract_title("#   Hello   "), "Hello")

    def test_multiline(self):
        md = "Some text\n\n# The Title\n\nMore text"
        self.assertEqual(extract_title(md), "The Title")

    def test_no_h1_raises(self):
        with self.assertRaises(Exception):
            extract_title("## Subheading\n\nPlain text")

    def test_empty_raises(self):
        with self.assertRaises(Exception):
            extract_title("")

    def test_only_h2_raises(self):
        with self.assertRaises(Exception):
            extract_title("## Not an h1")

    def test_h1_at_end(self):
        md = "Some paragraph\n\nAnother paragraph\n\n# Title at end"
        self.assertEqual(extract_title(md), "Title at end")

    def test_leading_newlines(self):
        md = "\n\n\n# Title after blanks"
        self.assertEqual(extract_title(md), "Title after blanks")
