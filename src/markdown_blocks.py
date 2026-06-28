import re
from enum import Enum

from leafnode import LeafNode
from parentnode import ParentNode
from textnode import text_node_to_html_node, text_to_textnodes


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    blocks = [block.strip() for block in blocks]
    blocks = [block for block in blocks if block]
    return blocks


def block_to_block_type(block: str) -> BlockType:
    lines = block.split("\n")

    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    if all(re.match(r"^\d+\. ", line) for line in lines):
        numbers = [int(line.split(".")[0]) for line in lines]
        if numbers == list(range(1, len(numbers) + 1)):
            return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def text_to_children(text: str) -> list[LeafNode]:
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]


def paragraph_to_html_node(block: str) -> ParentNode:
    text = block.replace("\n", " ")
    html_nodes = text_to_children(text)
    return ParentNode("p", html_nodes)


def heading_to_html_node(block: str) -> ParentNode:
    level = len(re.match(r"^#+", block).group())
    text = block[level + 1 :]
    html_nodes = text_to_children(text)
    return ParentNode(f"h{level}", html_nodes)


def code_to_html_node(block: str) -> ParentNode:
    content = block[3:-3]
    content = content.lstrip("\n")
    code_node = LeafNode("code", content)
    return ParentNode("pre", [code_node])


def quote_to_html_node(block: str) -> ParentNode:
    lines = block.split("\n")
    stripped = []
    for line in lines:
        if line.startswith("> "):
            stripped.append(line[2:])
        elif line.startswith(">"):
            stripped.append(line[1:])
        else:
            stripped.append(line)
    text = "\n".join(stripped)
    html_nodes = text_to_children(text)
    return ParentNode("blockquote", html_nodes)


def ulist_to_html_node(block: str) -> ParentNode:
    lines = block.split("\n")
    list_items = []
    for line in lines:
        item_text = line[2:]
        html_nodes = text_to_children(item_text)
        list_items.append(ParentNode("li", html_nodes))
    return ParentNode("ul", list_items)


def olist_to_html_node(block: str) -> ParentNode:
    lines = block.split("\n")
    list_items = []
    for line in lines:
        dot_index = line.index(".")
        item_text = line[dot_index + 2 :]
        html_nodes = text_to_children(item_text)
        list_items.append(ParentNode("li", html_nodes))
    return ParentNode("ol", list_items)


def block_to_html_node(block: str) -> ParentNode:
    block_type = block_to_block_type(block)

    match block_type:
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        case BlockType.HEADING:
            return heading_to_html_node(block)
        case BlockType.CODE:
            return code_to_html_node(block)
        case BlockType.QUOTE:
            return quote_to_html_node(block)
        case BlockType.UNORDERED_LIST:
            return ulist_to_html_node(block)
        case BlockType.ORDERED_LIST:
            return olist_to_html_node(block)


def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children)
