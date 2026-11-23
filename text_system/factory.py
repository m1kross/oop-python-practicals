"""Factory and navigator for structured text documents (SOLID-compliant)."""

from enum import Enum

from text_system.elements import Container, Heading, Paragraph, Root, TextElement


class TextType(Enum):
    """Supported text element types."""

    HEADING = "heading"
    PARAGRAPH = "paragraph"


class TextFactory:
    """Manages creation, navigation, and modification of a text tree."""

    def __init__(self, title: str = "Document") -> None:
        self._root = Root(title)
        self._current: Container = self._root

    @property
    def root(self) -> Root:
        return self._root

    @property
    def current(self) -> Container:
        return self._current

    def add_container(self, element_type: TextType, name: str, rank: int | None = None) -> Container:
        if element_type == TextType.HEADING:
            next_rank = rank if rank is not None else self._calc_next_rank()
            heading = Heading(name=name, rank=next_rank, parent=self._current)
            self._current.add_child(heading)
            self._current = heading
            return heading
        raise ValueError(f"Unsupported container type: {element_type.value}")

    def add_leaf(self, element_type: TextType, content: str | None) -> TextElement:
        if element_type == TextType.PARAGRAPH:
            paragraph = Paragraph(content)
            self._current.add_child(paragraph)
            return paragraph
        raise ValueError(f"Unsupported leaf type: {element_type.value}")

    # Backward-compatible methods for Practical 3
    def add_heading(self, name: str, rank: int = 0) -> None:
        self.add_container(TextType.HEADING, name=name, rank=rank)

    def add_paragraph(self, content: str | None) -> None:
        self.add_leaf(TextType.PARAGRAPH, content=content)

    def up(self) -> bool:
        if self._current.parent is not None:
            self._current = self._current.parent
            return True
        return False

    def pwd(self) -> str:
        parts: list[str] = []
        node: Container | None = self._current
        while node is not None and not node.is_root():
            parts.append(node.name)
            node = node.parent
        parts.reverse()
        return "/" + "/".join(parts)

    def cd(self, path: str) -> bool:
        if path == "/":
            self._current = self._root
            return True

        node: Container = self._root if path.startswith("/") else self._current
        segments = [seg for seg in path.split("/") if seg]

        for seg in segments:
            if seg == "..":
                if node.parent is not None:
                    node = node.parent
                continue
            found = next(
                (c for c in node.children if isinstance(c, Container) and c.name == seg),
                None,
            )
            if found is None:
                return False
            node = found

        self._current = node
        return True

    def cd_by_id(self, container_id: int) -> bool:
        found = self._find_container_by_id(self._root, container_id)
        if found is None:
            return False
        self._current = found
        return True

    def remove(self, elem_name: str | None = None) -> str | None:
        if elem_name is None:
            if self._current.is_root() or self._current.parent is None:
                return None
            target = self._current
            parent = self._current.parent
            parent.remove_child(target)
            self._current = parent
            return target.name

        for child in self._current.children:
            if isinstance(child, Container) and child.name == elem_name:
                self._current.remove_child(child)
                return child.name
            if isinstance(child, Paragraph) and child.content == elem_name:
                self._current.remove_child(child)
                return child.content
        return None

    def render(self, whole: bool = True, show_id: bool = False) -> str:
        target = self._root if whole else self._current
        return target.render(show_id=show_id)

    def _calc_next_rank(self) -> int:
        if isinstance(self._current, Heading):
            return self._current.rank + 1
        return 0

    def _find_container_by_id(self, node: Container, target_id: int) -> Container | None:
        if node.element_id == target_id:
            return node
        for child in node.children:
            if isinstance(child, Container):
                found = self._find_container_by_id(child, target_id)
                if found is not None:
                    return found
        return None

    def __str__(self) -> str:
        return self.render(whole=True, show_id=False)