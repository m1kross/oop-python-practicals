"""Structured text hierarchy using abstraction, inheritance, and polymorphism."""

from __future__ import annotations

from abc import ABC, abstractmethod


class TextElement(ABC):
    """Abstract base interface for all structured text nodes."""

    @abstractmethod
    def render(self) -> str:
        """Render the node and its nested content into a string."""


class Container(TextElement, ABC):
    """Abstract composite node that can contain child text elements."""

    def __init__(self, name: str, parent: Container | None = None) -> None:
        """Initialize a container node with a name and optional parent."""
        self._name: str = name
        self._parent: Container | None = parent
        self._children: list[TextElement] = []

    @property
    def name(self) -> str:
        """Return the container name."""
        return self._name

    @property
    def parent(self) -> Container | None:
        """Return the parent container, if any."""
        return self._parent

    @property
    def children(self) -> tuple[TextElement, ...]:
        """Return an immutable snapshot of child elements."""
        return tuple(self._children)

    def add_child(self, child: TextElement) -> None:
        """Append a child element to the container."""
        self._children.append(child)

    def is_root(self) -> bool:
        """Return True if this container has no parent."""
        return self._parent is None


class Leaf(TextElement, ABC):
    """Abstract terminal node that stores textual content without children."""

    def __init__(self, content: str | None) -> None:
        """Initialize a leaf node with optional string content."""
        self._content: str = content if content is not None else ""

    @property
    def content(self) -> str:
        """Return the leaf text content."""
        return self._content


class Root(Container):
    """Document root container."""

    def __init__(self, title: str) -> None:
        """Initialize the root document node with a title."""
        super().__init__(name=title, parent=None)

    def render(self) -> str:
        """Render document title and all child elements."""
        lines: list[str] = [f"Title: {self._name}"]
        for child in self._children:
            lines.append(child.render())
        return "\n".join(lines)


class Heading(Container):
    """Section heading container with nesting rank and indented children."""

    def __init__(self, name: str, rank: int = 0, parent: Container | None = None) -> None:
        """Initialize a heading with title, nesting rank, and parent container."""
        if rank < 0:
            raise ValueError("Heading rank must be non-negative.")
        super().__init__(name=name, parent=parent)
        self._rank: int = rank

    @property
    def rank(self) -> int:
        """Return the indentation/nesting rank of the heading."""
        return self._rank

    def render(self) -> str:
        """Render the heading and its nested children with rank-based indentation."""
        indent: str = "\t" * self._rank
        child_indent: str = "\t" * (self._rank + 1)
        lines: list[str] = [f"{indent}{self._name}"]
        for child in self._children:
            rendered_child: str = child.render()
            for part in rendered_child.splitlines():
                lines.append(f"{child_indent}{part}")
        return "\n".join(lines)


class Paragraph(Leaf):
    """Plain text paragraph leaf element."""

    def render(self) -> str:
        """Render paragraph content as a string."""
        return self._content
