"""Command-line and interactive input parser (SRP)."""

from dataclasses import dataclass
import shlex


@dataclass(frozen=True)
class ParsedCommand:
    """Represents a parsed command with selector, positional args, and options."""

    selector: str
    args: list[str]
    options: dict[str, str | bool]


class CommandParser:
    """Parses raw token lists or input strings into ParsedCommand objects."""

    @staticmethod
    def parse_tokens(tokens: list[str]) -> tuple[list[str], dict[str, str | bool]]:
        """Split tokens into positional arguments and --option/--flag pairs."""
        args: list[str] = []
        options: dict[str, str | bool] = {}

        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token.startswith("--") or (token.startswith("-") and len(token) == 2):
                key = token.lstrip("-")
                if i + 1 < len(tokens) and not tokens[i + 1].startswith("-"):
                    options[key] = tokens[i + 1]
                    i += 2
                else:
                    options[key] = True
                    i += 1
            else:
                args.append(token)
                i += 1

        return args, options

    @classmethod
    def parse_line(cls, line: str) -> ParsedCommand | None:
        """Parse an interactive input line supporting quoted arguments."""
        stripped = line.strip()
        if not stripped:
            return None

        tokens = shlex.split(stripped)
        selector = tokens[0].lower()
        args, options = cls.parse_tokens(tokens[1:])
        return ParsedCommand(selector=selector, args=args, options=options)