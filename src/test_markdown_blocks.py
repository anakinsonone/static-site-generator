import unittest

from markdown_blocks import BlockType, markdown_to_blocks, block_to_block_type


class TestMarkdownToBlocks(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_single_paragraph(self):
        blocks = markdown_to_blocks("Just one block")
        self.assertEqual(blocks, ["Just one block"])

    def test_blank_string(self):
        blocks = markdown_to_blocks("")
        self.assertEqual(blocks, [])

    def test_only_whitespace(self):
        blocks = markdown_to_blocks("  \n\n  \n\n  ")
        self.assertEqual(blocks, [])

    def test_leading_trailing_newlines(self):
        blocks = markdown_to_blocks("\n\nHello\n\n")
        self.assertEqual(blocks, ["Hello"])

    def test_multiple_paragraphs(self):
        blocks = markdown_to_blocks("P1\n\nP2\n\nP3")
        self.assertEqual(blocks, ["P1", "P2", "P3"])

    def test_unordered_list(self):
        blocks = markdown_to_blocks("- a\n- b\n- c")
        self.assertEqual(blocks, ["- a\n- b\n- c"])

    def test_excessive_newlines(self):
        blocks = markdown_to_blocks("A\n\n\n\nB")
        self.assertEqual(blocks, ["A", "B"])

    def test_heading_paragraph_list_mixed(self):
        md = "# Heading\n\nParagraph\n\n- item 1\n- item 2"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Heading",
                "Paragraph",
                "- item 1\n- item 2",
            ],
        )


class TestBlockToBlockType(unittest.TestCase):

    def test_heading_1(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)

    def test_heading_6(self):
        self.assertEqual(block_to_block_type("###### Heading"), BlockType.HEADING)

    def test_heading_too_many(self):
        self.assertEqual(block_to_block_type("####### Heading"), BlockType.PARAGRAPH)

    def test_heading_no_space(self):
        self.assertEqual(block_to_block_type("#Heading"), BlockType.PARAGRAPH)

    def test_heading_level_3(self):
        self.assertEqual(block_to_block_type("### Heading"), BlockType.HEADING)

    def test_code_block(self):
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_block_single_line(self):
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_block_no_closing(self):
        block = "```\ncode"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_quote_single_line(self):
        self.assertEqual(block_to_block_type("> Quote"), BlockType.QUOTE)

    def test_quote_multi_line(self):
        block = "> Line 1\n> Line 2"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_no_space(self):
        self.assertEqual(block_to_block_type(">Quote"), BlockType.QUOTE)

    def test_quote_mixed(self):
        block = "> Line 1\nNot a quote"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list_single(self):
        self.assertEqual(block_to_block_type("- Item"), BlockType.UNORDERED_LIST)

    def test_unordered_list_multi(self):
        block = "- A\n- B\n- C"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_wrong_prefix(self):
        block = "- A\n* B"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_single(self):
        self.assertEqual(block_to_block_type("1. Item"), BlockType.ORDERED_LIST)

    def test_ordered_list_multi(self):
        block = "1. A\n2. B\n3. C"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_wrong_start(self):
        block = "2. A\n3. B"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_skip_number(self):
        block = "1. A\n3. B"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_no_space(self):
        block = "1.Item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_plain_paragraph(self):
        self.assertEqual(
            block_to_block_type("Just some text."), BlockType.PARAGRAPH
        )

    def test_paragraph_with_mixed_content(self):
        self.assertEqual(
            block_to_block_type("Random **text** and _stuff_"),
            BlockType.PARAGRAPH,
        )


if __name__ == "__main__":
    unittest.main()
