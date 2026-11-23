"""Image element for structured text documents."""

from text_element import TextElement


class Image(TextElement):
    """Represents an image block with alternative text and source."""

    def __init__(self, alt_text: str, source: str) -> None:
        """Initialize an image with description and file path or URL."""
        self.alt_text = alt_text
        self.source = source

    def render(self) -> str:
        """Render the image placeholder with description and source."""
        return f"[Image: {self.alt_text} | {self.source}]"