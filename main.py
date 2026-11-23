"""Main entry point for Practical 4 (SOLID CLI)."""

import sys

from cli.characters_commands import CharactersContext, register_characters_commands
from cli.engine import CLIApp, CommandRegistry
from cli.parser import CommandParser
from cli.text_commands import register_text_commands
from text_system.factory import TextFactory


def choose_mode(options: dict[str, str | bool]) -> str:
    """Resolve CLI mode from startup flags or interactive dialog."""
    if "text" in options or "t" in options:
        return "text"
    if "chars" in options or "c" in options:
        return "chars"

    print("Select CLI mode:")
    print("  1. Text system (--text)")
    print("  2. Characters system (--chars)")
    choice = input("Enter 1 or 2 [1]: ").strip()
    return "chars" if choice == "2" else "text"


def main() -> None:
    """Parse startup arguments and launch the selected CLI mode."""
    _, options = CommandParser.parse_tokens(sys.argv[1:])
    mode = choose_mode(options)

    registry = CommandRegistry()
    if mode == "text":
        factory = TextFactory(title="My Document")
        register_text_commands(registry, factory)
        app = CLIApp(registry, mode_name="Text")
    else:
        ctx = CharactersContext()
        register_characters_commands(registry, ctx)
        app = CLIApp(registry, mode_name="Characters")

    app.run()


if __name__ == "__main__":
    main()