import unittest

from textnode import (
    TextNode,
    TextType,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
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
        matches = extract_markdown_links("Click [here](https://example.com) for more.")
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


class TestSplitNodes(unittest.TestCase):
    def test_split_images_single(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) in the middle",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" in the middle", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_multiple(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_no_images(self):
        node = TextNode("Just plain text with no images.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_images_at_start(self):
        node = TextNode(
            "![start](https://img.com/start.png) then some text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("start", TextType.IMAGE, "https://img.com/start.png"),
                TextNode(" then some text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_at_end(self):
        node = TextNode(
            "Some text then ![end](https://img.com/end.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Some text then ", TextType.TEXT),
                TextNode("end", TextType.IMAGE, "https://img.com/end.png"),
            ],
            new_nodes,
        )

    def test_split_images_only_image(self):
        node = TextNode(
            "![alone](https://img.com/alone.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("alone", TextType.IMAGE, "https://img.com/alone.png")],
            new_nodes,
        )

    def test_split_images_consecutive(self):
        node = TextNode(
            "![first](https://img.com/first.png)![second](https://img.com/second.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("first", TextType.IMAGE, "https://img.com/first.png"),
                TextNode("second", TextType.IMAGE, "https://img.com/second.png"),
            ],
            new_nodes,
        )

    def test_split_images_non_text_node_passthrough(self):
        node = TextNode("bold text", TextType.BOLD)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_images_mixed_node_types(self):
        node1 = TextNode(
            "Some text ![img](https://img.com/img.png) more", TextType.TEXT
        )
        node2 = TextNode("already italic", TextType.ITALIC)
        node3 = TextNode("No images here", TextType.TEXT)
        new_nodes = split_nodes_image([node1, node2, node3])
        self.assertListEqual(
            [
                TextNode("Some text ", TextType.TEXT),
                TextNode("img", TextType.IMAGE, "https://img.com/img.png"),
                TextNode(" more", TextType.TEXT),
                TextNode("already italic", TextType.ITALIC),
                TextNode("No images here", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_empty_text(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_images_ignores_links(self):
        node = TextNode(
            "This has a [link](https://boot.dev) but no image.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    # --- split_nodes_link ---

    def test_split_links_single(self):
        node = TextNode(
            "Click [here](https://example.com) for more.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Click ", TextType.TEXT),
                TextNode("here", TextType.LINK, "https://example.com"),
                TextNode(" for more.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_multiple(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_split_links_no_links(self):
        node = TextNode("Just plain text with no links.", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_links_at_start(self):
        node = TextNode(
            "[start](https://link.com/start) then some text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("start", TextType.LINK, "https://link.com/start"),
                TextNode(" then some text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_at_end(self):
        node = TextNode(
            "Some text then [end](https://link.com/end)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Some text then ", TextType.TEXT),
                TextNode("end", TextType.LINK, "https://link.com/end"),
            ],
            new_nodes,
        )

    def test_split_links_only_link(self):
        node = TextNode(
            "[alone](https://link.com/alone)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("alone", TextType.LINK, "https://link.com/alone")],
            new_nodes,
        )

    def test_split_links_consecutive(self):
        node = TextNode(
            "[first](https://link.com/first)[second](https://link.com/second)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("first", TextType.LINK, "https://link.com/first"),
                TextNode("second", TextType.LINK, "https://link.com/second"),
            ],
            new_nodes,
        )

    def test_split_links_non_text_node_passthrough(self):
        node = TextNode("italic text", TextType.ITALIC)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_links_mixed_node_types(self):
        node1 = TextNode("Click [here](https://ex.com) now", TextType.TEXT)
        node2 = TextNode("already bold", TextType.BOLD)
        node3 = TextNode("No links here", TextType.TEXT)
        new_nodes = split_nodes_link([node1, node2, node3])
        self.assertListEqual(
            [
                TextNode("Click ", TextType.TEXT),
                TextNode("here", TextType.LINK, "https://ex.com"),
                TextNode(" now", TextType.TEXT),
                TextNode("already bold", TextType.BOLD),
                TextNode("No links here", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_empty_text(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_links_ignores_images(self):
        node = TextNode(
            "This has an ![image](https://imgur.com/image.png) not a link.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)


if __name__ == "__main__":
    unittest.main()
