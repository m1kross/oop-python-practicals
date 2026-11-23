"""Entry point demonstrating the refactored game system."""

from ability import Ability
from character import Character
from game import Game
from logger import Logger


def main() -> None:
    """Run a sample combat session to verify refactored behavior."""
    logger = Logger(enabled=True)
    game = Game(logger=logger)

    warrior = Character(
        name="Arthas",
        max_hp=120,
        attack=20,
        armor=15,
        penetration=5,
        energy=30,
        logger=logger,
    )
    mage = Character(
        name="Jaina",
        max_hp=90,
        attack=14,
        armor=5,
        penetration=10,
        energy=40,
        logger=logger,
    )

    slash = Ability(name="Heavy Cleave", power=15, cost=15)
    frostbolt = Ability(name="Frostbolt", power=22, cost=20)

    warrior.add_ability(slash)
    mage.add_ability(frostbolt)

    game.basic_attack(warrior, mage)
    game.use_ability(mage, frostbolt, warrior)
    game.use_ability(warrior, slash, mage)

    print("\nFinal states:")
    print(warrior)
    print(mage)


if __name__ == "__main__":
    main()