import unittest

from textnode import (
    TextNode,
    TextType,
    text_node_to_html_node,
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
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

class TestExtractMarkdown(unittest.TestCase):

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_multiple(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        self.assertListEqual(
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
            matches,
        )

    def test_extract_markdown_images_no_images(self):
        matches = extract_markdown_images("This is plain text with no images.")
        self.assertListEqual([], matches)

    def test_extract_markdown_images_does_not_match_links(self):
        matches = extract_markdown_images(
            "This has a [link](https://boot.dev) but no image."
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            matches,
        )

    def test_extract_markdown_links_single(self):
        matches = extract_markdown_links(
            "Click [here](https://example.com) for more."
        )
        self.assertListEqual([("here", "https://example.com")], matches)

    def test_extract_markdown_links_no_links(self):
        matches = extract_markdown_links("Just plain text.")
        self.assertListEqual([], matches)

    def test_extract_markdown_links_does_not_match_images(self):
        matches = extract_markdown_links(
            "This has an ![image](https://imgur.com/image.png) not a link."
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_links_mixed(self):
        text = "An image ![img](https://img.com/a.png) and a [link](https://link.com)."
        self.assertListEqual(
            extract_markdown_images(text),
            [("img", "https://img.com/a.png")],
        )
        self.assertListEqual(
            extract_markdown_links(text),
            [("link", "https://link.com")],
        )

if __name__ == "__main__":
    unittest.main()
