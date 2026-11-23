"""Structured text elements using abstraction, inheritance, and polymorphism."""

from abc import ABC, abstractmethod


class TextElement(ABC):
    """Abstract base class for all structured text elements."""

    _id_counter: int = 0

    def __init__(self) -> None:
        TextElement._id_counter += 1
        self._id: int = TextElement._id_counter

    @property
    def element_id(self) -> int:
        return self._id

    @abstractmethod
    def render(self, show_id: bool = False) -> str:
        """Render element to string."""


class Container(TextElement, ABC):
    """Abstract container element that holds child elements."""

    def __init__(self, name: str, parent: "Container | None" = None) -> None:
        super().__init__()
        self._name = name
        self._parent = parent
        self._children: list[TextElement] = []

    @property
    def name(self) -> str:
        return self._name

    @property
    def parent(self) -> "Container | None":
        return self._parent

    @property
    def children(self) -> tuple[TextElement, ...]:
        return tuple(self._children)

    def add_child(self, child: TextElement) -> None:
        self._children.append(child)

    def remove_child(self, child: TextElement) -> bool:
        if child in self._children:
            self._children.remove(child)
            return True
        return False

    def is_root(self) -> bool:
        return self._parent is None


class Leaf(TextElement, ABC):
    """Abstract leaf element with text content and no children."""

    def __init__(self, content: str | None) -> None:
        super().__init__()
        self._content = "" if content is None else content

    @property
    def content(self) -> str:
        return self._content


class Root(Container):
    """Root container of a structured document."""

    def __init__(self, name: str) -> None:
        super().__init__(name=name, parent=None)

    def render(self, show_id: bool = False) -> str:
        prefix = f"[#{self.element_id}] " if show_id else ""
        lines = [f"{prefix}Title: {self._name}"]
        for child in self._children:
            lines.append(child.render(show_id=show_id))
        return "\n".join(lines)


class Heading(Container):
    """Heading container with nesting rank."""

    def __init__(self, name: str, rank: int = 0, parent: Container | None = None) -> None:
        super().__init__(name=name, parent=parent)
        self._rank = max(0, rank)

    @property
    def rank(self) -> int:
        return self._rank

    def render(self, show_id: bool = False) -> str:
        indent = "\t" * self._rank
        child_indent = "\t" * (self._rank + 1)
        prefix = f"[#{self.element_id}] " if show_id else ""
        lines = [f"{indent}{prefix}{self._name}"]
        for child in self._children:
            rendered = child.render(show_id=show_id)
            if isinstance(child, Heading):
                lines.append(rendered)
            else:
                lines.append(f"{child_indent}{rendered}")
        return "\n".join(lines)


class Paragraph(Leaf):
    """Leaf element representing a text paragraph."""

    def render(self, show_id: bool = False) -> str:
        prefix = f"[#{self.element_id}] " if show_id else ""
        return f"{prefix}{self._content}"