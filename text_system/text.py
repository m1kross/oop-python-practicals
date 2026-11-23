"""Document container class managing text elements."""

from heading import Heading
from text_element import TextElement


class Text:
    """Container holding ordered text elements and generating text/TOC."""

    def __init__(self, elements: list[TextElement] | None = None) -> None:
        """Initialize the container with an optional list of elements."""
        self.elements: list[TextElement] = list(elements) if elements else []

    def add_element(self, element: TextElement, index: int | None = None) -> None:
        """Add an element to the end or at a specific position."""
        if index is None:
            self.elements.append(element)
        else:
            self.elements.insert(index, element)

    def remove_element(self, index: int) -> TextElement:
        """Remove and return the element at the given index."""
        return self.elements.pop(index)

    def move_element(self, current_index: int, target_index: int) -> None:
        """Move an element from current_index to target_index."""
        element = self.elements.pop(current_index)
        self.elements.insert(target_index, element)

    def get_table_of_contents(self) -> str:
        """Build an indented table of contents from headings only."""
        lines = [
            element.to_toc_entry()
            for element in self.elements
            if isinstance(element, Heading)
        ]
        return "\n".join(lines)

    def __str__(self) -> str:
        """Render all contained elements into a single string."""
        return "\n\n".join(str(element) for element in self.elements)