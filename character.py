"""Character domain model with encapsulated state and combat calculations."""

from ability import Ability
from logger import Logger


class Character:
    """Represents a game character with encapsulated stats and abilities."""

    def __init__(
        self,
        name: str,
        max_hp: int = 100,
        attack: int = 15,
        armor: int = 10,
        penetration: int = 0,
        energy: int = 50,
        logger: Logger | None = None,
    ) -> None:
        """Initialize a character with validated stats and optional logger."""
        if not name.strip():
            raise ValueError("Character name cannot be empty.")
        if max_hp <= 0:
            raise ValueError("Max HP must be positive.")

        self._name = name
        self._max_hp = max_hp
        self._hp = max_hp
        self._energy = 0
        self.attack = attack
        self.armor = armor
        self.penetration = penetration
        self.energy = energy
        self._abilities: list[Ability] = []
        self._logger = logger if logger is not None else Logger()

    @property
    def name(self) -> str:
        """Return character name."""
        return self._name

    @property
    def hp(self) -> int:
        """Return current health points."""
        return self._hp

    @property
    def is_alive(self) -> bool:
        """Return True if character still has health points."""
        return self._hp > 0

    @property
    def attack(self) -> int:
        """Return base attack value."""
        return self._attack

    @attack.setter
    def attack(self, value: int) -> None:
        """Set non-negative base attack."""
        if value < 0:
            raise ValueError("Attack cannot be negative.")
        self._attack = value

    @property
    def armor(self) -> int:
        """Return armor/resistance value."""
        return self._armor

    @armor.setter
    def armor(self, value: int) -> None:
        """Set non-negative armor value."""
        if value < 0:
            raise ValueError("Armor cannot be negative.")
        self._armor = value

    @property
    def penetration(self) -> int:
        """Return armor penetration value."""
        return self._penetration

    @penetration.setter
    def penetration(self, value: int) -> None:
        """Set non-negative penetration value."""
        if value < 0:
            raise ValueError("Penetration cannot be negative.")
        self._penetration = value

    @property
    def energy(self) -> int:
        """Return current energy points."""
        return self._energy

    @energy.setter
    def energy(self, value: int) -> None:
        """Set energy clamped to non-negative range."""
        self._energy = max(0, value)

    @property
    def abilities(self) -> tuple[Ability, ...]:
        """Return an immutable snapshot of character abilities."""
        return tuple(self._abilities)

    def add_ability(self, ability: Ability) -> None:
        """Add an ability to the character's repertoire."""
        self._abilities.append(ability)
        self._logger.log(f"{self._name} learned ability '{ability.name}'.")

    def spend_energy(self, amount: int) -> bool:
        """Spend energy if enough is available; return True on success."""
        if amount < 0:
            raise ValueError("Energy amount cannot be negative.")
        if self._energy < amount:
            self._logger.log(
                f"{self._name} does not have enough energy ({self._energy}/{amount})."
            )
            return False
        self._energy -= amount
        return True

    def restore_energy(self, amount: int) -> None:
        """Restore character energy."""
        if amount < 0:
            raise ValueError("Energy amount cannot be negative.")
        self._energy += amount

    def calculate_incoming_damage(self, raw_damage: int, attacker_penetration: int = 0) -> int:
        """Compute actual damage after applying penetration and armor mitigation."""
        effective_pen = min(self._armor, max(0, attacker_penetration))
        effective_armor = max(0, self._armor - effective_pen)
        mitigated = max(1, int(raw_damage * (100 / (100 + effective_armor))))
        return max(0, mitigated) if raw_damage > 0 else 0

    def take_damage(self, raw_damage: int, attacker_penetration: int = 0) -> int:
        """Apply incoming damage through encapsulation rules and return final damage."""
        if not self.is_alive:
            self._logger.log(f"{self._name} is already defeated.")
            return 0

        damage_taken = self.calculate_incoming_damage(raw_damage, attacker_penetration)
        self._hp = max(0, self._hp - damage_taken)
        self._logger.log(
            f"{self._name} took {damage_taken} damage (HP: {self._hp}/{self._max_hp})."
        )
        if not self.is_alive:
            self._logger.log(f"{self._name} has been defeated!")
        return damage_taken

    def __str__(self) -> str:
        """Return readable summary of the character."""
        return (
            f"Character(name={self._name!r}, hp={self._hp}/{self._max_hp}, "
            f"energy={self._energy}, armor={self._armor})"
        )