"""Ability domain model for game characters."""


class Ability:
    """Represents a character ability with damage power and energy cost."""

    def __init__(self, name: str, power: int, cost: int = 10) -> None:
        """Initialize an ability with validated name, power, and cost."""
        if not name.strip():
            raise ValueError("Ability name cannot be empty.")
        self._name = name
        self.power = power
        self.cost = cost

    @property
    def name(self) -> str:
        """Return ability name."""
        return self._name

    @property
    def power(self) -> int:
        """Return base power of the ability."""
        return self._power

    @power.setter
    def power(self, value: int) -> None:
        """Set non-negative ability power."""
        if value < 0:
            raise ValueError("Ability power cannot be negative.")
        self._power = value

    @property
    def cost(self) -> int:
        """Return energy cost of the ability."""
        return self._cost

    @cost.setter
    def cost(self, value: int) -> None:
        """Set non-negative energy cost."""
        if value < 0:
            raise ValueError("Ability cost cannot be negative.")
        self._cost = value