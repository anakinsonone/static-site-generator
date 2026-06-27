import unittest

from textnode import extract_markdown_images, extract_markdown_links


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


if __name__ == "__main__":
    unittest.main()
