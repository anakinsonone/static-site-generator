import unittest
from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    # 1. Test basic parent with one child
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    # 2. Test nested parents (grandchildren)
    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    # 3. Test a parent with multiple children of different types
    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    # 4. Test that it works with HTML attributes (props)
    def test_to_html_with_props(self):
        node = ParentNode("p", [LeafNode("b", "Bold text")], {"class": "text-bold"})
        self.assertEqual(
            node.to_html(),
            '<p class="text-bold"><b>Bold text</b></p>',
        )

    # 5. Test Error Handling: Missing Tag
    def test_missing_tag_raises_error(self):
        node = ParentNode(None, [LeafNode("b", "Bold text")])
        with self.assertRaises(ValueError):
            node.to_html()

    # 6. Test Error Handling: Missing Children
    def test_missing_children_raises_error(self):
        # We have to bypass the type hints intentionally to test this
        node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()


if __name__ == "__main__":
    unittest.main()
