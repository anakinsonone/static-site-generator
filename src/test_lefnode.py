import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    # 1. The starter test: Basic tag with a value
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    # 2. Test rendering with properties
    def test_leaf_to_html_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )

    # 3. Test that passing no tag returns raw text
    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just plain text")
        self.assertEqual(node.to_html(), "Just plain text")

    # 4. Test that creating a LeafNode without a value raises an error
    def test_leaf_no_value_raises_error(self):
        # self.assertRaises is a special unittest method for catching expected errors
        with self.assertRaises(ValueError):
            node = LeafNode("p", None)


if __name__ == "__main__":
    unittest.main()
