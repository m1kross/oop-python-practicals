"""Item domain model for game characters."""


class Item:
    """Represents an equippable or usable item."""

    def __init__(
        self,
        name: str,
        bonus_attack: int = 0,
        bonus_armor: int = 0,
        heal_power: int = 0,
    ) -> None:
        if not name.strip():
            raise ValueError("Item name cannot be empty.")
        self._name = name
        self._bonus_attack = max(0, bonus_attack)
        self._bonus_armor = max(0, bonus_armor)
        self._heal_power = max(0, heal_power)

    @property
    def name(self) -> str:
        return self._name

    @property
    def bonus_attack(self) -> int:
        return self._bonus_attack

    @property
    def bonus_armor(self) -> int:
        return self._bonus_armor

    @property
    def heal_power(self) -> int:
        return self._heal_power

    def __str__(self) -> str:
        return (
            f"Item(name={self._name!r}, +atk={self._bonus_attack}, "
            f"+armor={self._bonus_armor}, heal={self._heal_power})"
        )