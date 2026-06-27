import unittest

from textnode import (
    TextNode,
    TextType,
    text_node_to_html_node,
    split_nodes_delimiter,
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

    def test_code(self):
        node = TextNode(
            "This is text with a `code block` word",
            TextType.TEXT,
        )

        self.assertEqual(
            split_nodes_delimiter([node], "`", TextType.CODE),
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_bold(self):
        node = TextNode(
            "This is **bold** text",
            TextType.TEXT,
        )

        self.assertEqual(
            split_nodes_delimiter([node], "**", TextType.BOLD),
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_multiple(self):
        node = TextNode(
            "a `code` and `more code`",
            TextType.TEXT,
        )

        self.assertEqual(
            split_nodes_delimiter([node], "`", TextType.CODE),
            [
                TextNode("a ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" and ", TextType.TEXT),
                TextNode("more code", TextType.CODE),
            ],
        )

    def test_invalid_markdown(self):
        node = TextNode(
            "This is `broken markdown",
            TextType.TEXT,
        )

        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_non_text_nodes_unchanged(self):
        node = TextNode(
            "already bold",
            TextType.BOLD,
        )

        self.assertEqual(
            split_nodes_delimiter([node], "`", TextType.CODE),
            [node],
        )


if __name__ == "__main__":
    unittest.main()
