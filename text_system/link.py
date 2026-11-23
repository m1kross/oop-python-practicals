"""Link element for structured text documents."""

from text_element import TextElement


class Link(TextElement):
    """Represents a hyperlink with anchor text and URL."""

    def __init__(self, label: str, url: str) -> None:
        """Initialize a link with display label and target URL."""
        self.label = label
        self.url = url

    def render(self) -> str:
        """Render the link as text with URL."""
        return f"{self.label} ({self.url})"