import unittest

from textnode import (
    TextNode,
    TextType,
    text_node_to_html_node,
)


class TestTextNodeToHTMLNode(unittest.TestCase):

    def test_text(self):
        node = TextNode(
            "This is a text node",
            TextType.TEXT,
        )

        html = text_node_to_html_node(node)

        self.assertEqual(html.tag, None)
        self.assertEqual(html.value, "This is a text node")

    def test_bold(self):
        node = TextNode(
            "bold text",
            TextType.BOLD,
        )

        html = text_node_to_html_node(node)

        self.assertEqual(html.tag, "b")
        self.assertEqual(html.value, "bold text")

    def test_italic(self):
        node = TextNode(
            "italic text",
            TextType.ITALIC,
        )

        html = text_node_to_html_node(node)

        self.assertEqual(html.tag, "i")
        self.assertEqual(html.value, "italic text")

    def test_code(self):
        node = TextNode(
            "print('hello')",
            TextType.CODE,
        )

        html = text_node_to_html_node(node)

        self.assertEqual(html.tag, "code")
        self.assertEqual(html.value, "print('hello')")

    def test_link(self):
        node = TextNode(
            "Boot.dev",
            TextType.LINK,
            "https://www.boot.dev",
        )

        html = text_node_to_html_node(node)

        self.assertEqual(html.tag, "a")
        self.assertEqual(html.value, "Boot.dev")
        self.assertEqual(
            html.props,
            {"href": "https://www.boot.dev"},
        )

    def test_image(self):
        node = TextNode(
            "logo",
            TextType.IMAGE,
            "https://example.com/logo.png",
        )

        html = text_node_to_html_node(node)

        self.assertEqual(html.tag, "img")
        self.assertEqual(html.value, "")
        self.assertEqual(
            html.props,
            {
                "src": "https://example.com/logo.png",
                "alt": "logo",
            },
        )

    def test_invalid_type(self):
        node = TextNode(
            "hello",
            "INVALID",
        )

        with self.assertRaises(Exception):
            text_node_to_html_node(node)


if __name__ == "__main__":
    unittest.main()
