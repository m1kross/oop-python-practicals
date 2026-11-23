"""Logging utilities for game events."""


class Logger:
    """Encapsulates event output so domain classes do not depend on print directly."""

    def __init__(self, enabled: bool = True) -> None:
        """Initialize logger with an enabled flag."""
        self._enabled = enabled

    @property
    def enabled(self) -> bool:
        """Return whether logging is active."""
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool) -> None:
        """Enable or disable log output."""
        self._enabled = bool(value)

    def log(self, message: str) -> None:
        """Record or print a message if logging is enabled."""
        if self._enabled:
            print(f"[LOG] {message}")