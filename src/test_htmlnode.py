import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_props_to_html_single(self):
        node = HTMLNode("a", "Click me", None, {"href": "https://google.com"})
        self.assertEqual(node.props_to_html(), ' href="https://google.com"')

    def test_props_to_html_none(self):
        node = HTMLNode("p", "Just some text")
        self.assertEqual(node.props_to_html(), "")

if __name__ == "__main__":
    unittest.main()
