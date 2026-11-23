"""Turn and combat orchestration for the game system."""

from game_system.ability import Ability
from game_system.character import Character
from game_system.logger import Logger


class Game:
    """Coordinates turns, ability usage, damage application, and logging."""

    def __init__(self, logger: Logger | None = None) -> None:
        """Initialize game controller with a logger."""
        self._logger = logger if logger is not None else Logger()
        self._turn = 0

    @property
    def turn(self) -> int:
        """Return current turn number."""
        return self._turn

    def basic_attack(self, attacker: Character, target: Character) -> int:
        """Execute a basic attack from attacker to target."""
        self._turn += 1
        self._logger.log(f"--- Turn {self._turn}: {attacker.name} attacks {target.name} ---")
        if not attacker.is_alive or not target.is_alive:
            self._logger.log("Attack skipped: one of the characters is defeated.")
            return 0

        attacker.restore_energy(5)
        return target.take_damage(attacker.attack, attacker.penetration)

    def use_ability(self, actor: Character, ability: Ability, target: Character) -> int:
        """Validate and execute an ability used by actor against target."""
        self._turn += 1
        self._logger.log(
            f"--- Turn {self._turn}: {actor.name} uses '{ability.name}' on {target.name} ---"
        )
        if not actor.is_alive or not target.is_alive:
            self._logger.log("Ability skipped: one of the characters is defeated.")
            return 0

        if ability not in actor.abilities:
            self._logger.log(f"{actor.name} does not know ability '{ability.name}'.")
            return 0

        if not actor.spend_energy(ability.cost):
            return 0

        total_raw_damage = actor.attack + ability.power
        return target.take_damage(total_raw_damage, actor.penetration)