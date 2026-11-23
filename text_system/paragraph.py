"""Paragraph element for structured text documents."""

from text_element import TextElement


class Paragraph(TextElement):
    """Represents a plain text paragraph."""

    def __init__(self, content: str) -> None:
        """Initialize a paragraph with text content."""
        self.content = content

    def render(self) -> str:
        """Return the paragraph text."""
        return self.content