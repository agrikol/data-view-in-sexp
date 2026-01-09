from typing import List
from rich.text import Text
from rich.console import Console
from src.shared.model import Node
from typing import List
from src.visualizer.styles import TreeStyle, UNICODE_STYLE, ASCII_STYLE


class TreeRenderer:
    def __init__(self, askii=False):
        style = TreeStyle = ASCII_STYLE if askii else UNICODE_STYLE
        self.style = style

    def render(self, root: "Node") -> None:
        console = Console()
        text = Text()
        self._render_node(root, text, pipes=[], is_last=True)
        console.print(text)

    def _render_node(
        self,
        node: "Node",
        out: Text,
        pipes: List[bool],
        is_last: bool,
    ) -> None:
        for has_pipe in pipes[:-1]:
            out.append(
                self.style.trunk if has_pipe else self.style.space,
                style="#B6B6B6",
            )

        if pipes:
            out.append(
                self.style.leaf if is_last else self.style.branch,
                style="#B6B6B6",
            )

        out.append(node.name, style="#5BB8FF")

        if node.attrs:
            for k, v in node.attrs.items():
                out.append(" ")
                out.append(f":{k}=", style="#FF5555")
                out.append(str(v), style="#DDB500")

        out.append("\n")

        if node.is_leaf:
            for has_pipe in pipes:
                out.append(
                    self.style.trunk if has_pipe else self.style.space,
                    style="#B6B6B6",
                )
            out.append(self.style.leaf, style="#B6B6B6")
            out.append(str(node.scalar), style="#3ED77B")
            out.append("\n")
            return

        count = len(node.children)
        for i, child in enumerate(node.children):
            last = i == count - 1
            self._render_node(
                child,
                out,
                pipes=pipes + [not last],
                is_last=last,
            )
