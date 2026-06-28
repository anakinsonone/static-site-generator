import re
from enum import Enum


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
