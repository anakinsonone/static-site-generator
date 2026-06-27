import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    # 1. Test exact equality (URL defaults to None)
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    # 2. Test inequality when the text_type is different
    def test_not_eq_text_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    # 3. Test inequality when the text string itself is different
    def test_not_eq_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a DIFFERENT text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    # 4. Test equality when a URL is provided
    def test_eq_with_url(self):
        node = TextNode("This is a text node", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.LINK, "https://www.boot.dev")
        self.assertEqual(node, node2)

    # 5. Test inequality when only one node has a URL
    def test_not_eq_url(self):
        node = TextNode("This is a text node", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.LINK) # Defaults to None
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()
