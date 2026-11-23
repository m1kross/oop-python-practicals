"""Base element definition for structured text documents."""


class TextElement:
    """Base class for any element stored inside a Text container."""

    def render(self) -> str:
        """Render the element into its text representation."""
        raise NotImplementedError("Subclasses must implement render().")

    def __str__(self) -> str:
        """Return the string representation of the element."""
        return self.render()