"""Demo script for structured text hierarchy and TextFactory."""

from text_system.factory import TextFactory


def main() -> None:
    """Run sample document construction and console rendering."""
    doc = TextFactory("Test Document")
    doc.add_paragraph("Some thoughts...")
    doc.add_heading("Top:", rank=0)
    doc.add_paragraph("This is a line.")
    doc.add_paragraph("This is another line.")
    doc.add_heading("Inner:", rank=1)
    doc.add_paragraph("This is an inner line.")
    doc.up()
    doc.add_paragraph("Some closure...")
    print(doc)


if __name__ == "__main__":
    main()