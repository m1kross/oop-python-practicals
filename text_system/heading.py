"""Heading element for structured text documents."""

from text_element import TextElement


class Heading(TextElement):
    """Represents a section heading with a nesting level."""

    def __init__(self, title: str, level: int = 1) -> None:
        """Initialize a heading with title text and level."""
        self.title = title
        self.level = max(1, level)

    def render(self) -> str:
        """Render the heading as markdown-style text."""
        prefix = "#" * self.level
        return f"{prefix} {self.title}"

    def to_toc_entry(self) -> str:
        """Format the heading as an indented table of contents entry."""
        indent = "  " * (self.level - 1)
        return f"{indent}{self.title}"