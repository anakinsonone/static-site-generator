from typing import override
from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    @override
    def __init__(
        self, tag: str, children: list[HTMLNode], props: dict[str, str] | None = None
    ) -> None:
        super().__init__(tag=tag, value=None, children=children, props=props)

    @override
    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")

        if self.children is None:
            raise ValueError("ParentNode must have children")

        children_html = "".join([child.to_html() for child in self.children])

        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
