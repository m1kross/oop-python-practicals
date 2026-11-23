"""Factory/builder facade for constructing structured text trees."""

from __future__ import annotations

from text_system.elements import Container, Heading, Paragraph, Root


class TextFactory:
    """Manages creation and tree navigation for structured text elements."""

    def __init__(self, title: str) -> None:
        """Initialize the factory with a root document node."""
        self._root: Root = Root(title=title)
        self._current: Container = self._root

    def add_heading(self, name: str, rank: int = 0) -> None:
        """Create a heading under the current node and move focus into it."""
        heading = Heading(name=name, rank=rank, parent=self._current)
        self._current.add_child(heading)
        self._current = heading

    def add_paragraph(self, content: str | None) -> None:
        """Create a paragraph under the current node."""
        self._current.add_child(Paragraph(content=content))

    def up(self) -> None:
        """Move current focus up to the parent container if not at root."""
        if self._current.is_root():
            print("You are already in root.")
            return
        if self._current.parent is not None:
            self._current = self._current.parent

    def render(self) -> str:
        """Render the full document starting from the root node."""
        return self._root.render()

    def __str__(self) -> str:
        """Return the rendered string representation of the document."""
        return self.render()
