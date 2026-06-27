from typing import override


class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list["HTMLNode"] | None = None,
        props: dict[str, str] | None = None,
    ) -> None:
        self.tag: str | None = tag
        self.value: str | None = value
        self.children: list[HTMLNode] | None = children
        self.props: dict[str, str] | None = props

    def to_html(self) -> None:
        raise NotImplementedError("not implemented")

    def props_to_html(self) -> str:
        if self.props is None:
            return ""

        props_html = ""
        for key, value in self.props.items():
            props_html += f' {key}="{value}"'

        return props_html

    @override
    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
