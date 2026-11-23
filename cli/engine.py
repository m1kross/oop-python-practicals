"""Dynamic command registry and interactive REPL engine (OCP, DIP)."""

from collections.abc import Callable

from cli.parser import CommandParser, ParsedCommand

CommandHandler = Callable[[ParsedCommand], None]


class CommandRegistry:
    """Stores and dispatches commands by selector without modifying core logic."""

    def __init__(self) -> None:
        self._commands: dict[str, tuple[CommandHandler, str]] = {}

    def add_command(self, selector: str, handler: CommandHandler, description: str = "") -> None:
        """Register a command selector with its handler."""
        self._commands[selector.lower()] = (handler, description)

    def execute(self, parsed: ParsedCommand) -> bool:
        """Execute a registered command; return False if not found."""
        entry = self._commands.get(parsed.selector)
        if entry is None:
            return False
        handler, _ = entry
        handler(parsed)
        return True

    def list_help(self) -> str:
        """Return formatted list of all registered commands."""
        lines = ["Available commands:"]
        for name, (_, desc) in self._commands.items():
            lines.append(f"  {name:<10} - {desc}")
        return "\n".join(lines)


class CLIApp:
    """Interactive console loop for executing registered commands."""

    def __init__(self, registry: CommandRegistry, mode_name: str) -> None:
        self._registry = registry
        self._mode_name = mode_name
        self._running = True

        self._registry.add_command("help", lambda _: print(self._registry.list_help()), "Show commands")
        self._registry.add_command("exit", self._stop, "Exit the CLI")

    def _stop(self, _: ParsedCommand) -> None:
        self._running = False
        print("Exiting CLI...")

    def run(self) -> None:
        """Start interactive prompt loop."""
        print(f"=== {self._mode_name} CLI Mode (type 'help' for commands, 'exit' to quit) ===")
        while self._running:
            try:
                raw = input("> ")
            except (EOFError, KeyboardInterrupt):
                print("\nExiting CLI...")
                break

            try:
                parsed = CommandParser.parse_line(raw)
            except ValueError as err:
                print(f"Parse error: {err}")
                continue

            if parsed is None:
                continue

            try:
                if not self._registry.execute(parsed):
                    print(f"Unknown command: '{parsed.selector}'. Type 'help'.")
            except Exception as err:
                print(f"Error: {err}")