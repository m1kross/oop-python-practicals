"""CLI commands for the Characters system."""

from cli.engine import CommandRegistry
from cli.parser import ParsedCommand
from game_system.ability import Ability
from game_system.character import Character
from game_system.game import Game
from game_system.item import Item
from game_system.logger import Logger


class CharactersContext:
    """Holds Characters domain entities indexed by unique IDs."""

    def __init__(self) -> None:
        self.logger = Logger(enabled=True)
        self.game = Game(logger=self.logger)
        self.characters: dict[int, Character] = {}
        self.items: dict[int, Item] = {}
        self.abilities: dict[int, Ability] = {}
        self._char_seq = 0
        self._item_seq = 0
        self._ability_seq = 0

    def next_char_id(self) -> int:
        self._char_seq += 1
        return self._char_seq

    def next_item_id(self) -> int:
        self._item_seq += 1
        return self._item_seq

    def next_ability_id(self) -> int:
        self._ability_seq += 1
        return self._ability_seq

    def find_character(self, ref: str) -> tuple[int, Character] | None:
        return self._find_by_ref(self.characters, ref)

    def find_item(self, ref: str) -> tuple[int, Item] | None:
        return self._find_by_ref(self.items, ref)

    def find_ability(self, ref: str) -> tuple[int, Ability] | None:
        return self._find_by_ref(self.abilities, ref)

    @staticmethod
    def _find_by_ref(store: dict[int, object], ref: str) -> tuple[int, object] | None:
        if ref.isdigit():
            key = int(ref)
            if key in store:
                return key, store[key]
        ref_lower = ref.lower()
        for obj_id, obj in store.items():
            if getattr(obj, "name", "").lower() == ref_lower:
                return obj_id, obj
        return None


def _read_int(prompt: str, default: int) -> int:
    raw = input(f"{prompt} [{default}]: ").strip()
    return int(raw) if raw else default


def register_characters_commands(registry: CommandRegistry, ctx: CharactersContext) -> None:
    """Register Characters CLI commands into the registry."""

    def cmd_create(cmd: ParsedCommand) -> None:
        if not cmd.args:
            print("Usage: create <char|item|ability>")
            return
        kind = cmd.args[0].lower()

        if kind == "char":
            name = input("Character name: ").strip()
            max_hp = _read_int("Max HP", 100)
            attack = _read_int("Attack", 15)
            armor = _read_int("Armor", 10)
            penetration = _read_int("Penetration", 0)
            energy = _read_int("Energy", 50)
            cid = ctx.next_char_id()
            ctx.characters[cid] = Character(
                name=name,
                max_hp=max_hp,
                attack=attack,
                armor=armor,
                penetration=penetration,
                energy=energy,
                logger=ctx.logger,
            )
            print(f"Created character [#{cid}] {name}")

        elif kind == "item":
            name = input("Item name: ").strip()
            bonus_atk = _read_int("Bonus attack", 0)
            bonus_armor = _read_int("Bonus armor", 0)
            heal_power = _read_int("Heal power", 0)
            iid = ctx.next_item_id()
            ctx.items[iid] = Item(
                name=name,
                bonus_attack=bonus_atk,
                bonus_armor=bonus_armor,
                heal_power=heal_power,
            )
            print(f"Created item [#{iid}] {name}")

        elif kind == "ability":
            name = input("Ability name: ").strip()
            power = _read_int("Power", 20)
            cost = _read_int("Energy cost", 15)
            aid = ctx.next_ability_id()
            ctx.abilities[aid] = Ability(name=name, power=power, cost=cost)
            print(f"Created ability [#{aid}] {name}")

        else:
            print("Unknown type. Use: create <char|item|ability>")

    def cmd_add(cmd: ParsedCommand) -> None:
        char_ref = cmd.options.get("char_id")
        obj_ref = cmd.options.get("id")
        if not isinstance(char_ref, str) or not isinstance(obj_ref, str):
            print("Usage: add --char_id <id/name> --id <id/name>")
            return

        char_match = ctx.find_character(char_ref)
        if char_match is None:
            print(f"Character '{char_ref}' not found.")
            return
        _, char = char_match

        ability_match = ctx.find_ability(obj_ref)
        if ability_match is not None:
            _, ability = ability_match
            char.add_ability(ability)
            return

        item_match = ctx.find_item(obj_ref)
        if item_match is not None:
            _, item = item_match
            char.add_item(item)
            return

        print(f"Item or ability '{obj_ref}' not found.")

    def cmd_act(cmd: ParsedCommand) -> None:
        if len(cmd.args) < 3:
            print("Usage: act <attack|heal|ability> <actor> <target> [--id <id/name>]")
            return
        action, actor_ref, target_ref = cmd.args[0].lower(), cmd.args[1], cmd.args[2]

        actor_match = ctx.find_character(actor_ref)
        target_match = ctx.find_character(target_ref)
        if actor_match is None or target_match is None:
            print("Actor or target character not found.")
            return
        _, actor = actor_match
        _, target = target_match

        if action == "attack":
            ctx.game.basic_attack(actor, target)
        elif action == "heal":
            heal_amount = 20
            obj_ref = cmd.options.get("id")
            if isinstance(obj_ref, str):
                item_match = ctx.find_item(obj_ref)
                if item_match is not None:
                    _, item = item_match
                    heal_amount = item.heal_power or heal_amount
            target.heal(heal_amount)
        elif action == "ability":
            ab_ref = cmd.options.get("id")
            if not isinstance(ab_ref, str):
                print("Please specify ability via --id <id/name>")
                return
            ab_match = ctx.find_ability(ab_ref)
            if ab_match is None:
                print(f"Ability '{ab_ref}' not found.")
                return
            _, ability = ab_match
            ctx.game.use_ability(actor, ability, target)
        else:
            print("Unknown action. Use: attack, heal, or ability.")

    def cmd_ls(cmd: ParsedCommand) -> None:
        if not cmd.args:
            print("Usage: ls <char|item|ability> [--id <id/name>]")
            return
        kind = cmd.args[0].lower()
        target_ref = cmd.options.get("id")

        if kind == "char":
            if isinstance(target_ref, str):
                match = ctx.find_character(target_ref)
                if match is None:
                    print(f"Character '{target_ref}' not found.")
                    return
                cid, c = match
                print(f"[#{cid}] {c}")
                print(f"  Penetration: {c.penetration}, Alive: {c.is_alive}")
                print(f"  Abilities: {[a.name for a in c.abilities]}")
                print(f"  Items: {[i.name for i in c.items]}")
            else:
                if not ctx.characters:
                    print("No characters yet.")
                for cid, c in ctx.characters.items():
                    print(f"[#{cid}] {c.name} (HP: {c.hp}/{c.max_hp}, Energy: {c.energy})")

        elif kind == "item":
            if isinstance(target_ref, str):
                match = ctx.find_item(target_ref)
                if match is None:
                    print(f"Item '{target_ref}' not found.")
                    return
                iid, it = match
                owners = [c.name for c in ctx.characters.values() if it in c.items]
                print(f"[#{iid}] {it} | Owners: {owners or 'anyone'}")
            else:
                if not ctx.items:
                    print("No items yet.")
                for iid, it in ctx.items.items():
                    owners = [c.name for c in ctx.characters.values() if it in c.items]
                    print(f"[#{iid}] {it.name} | Used by: {owners or 'anyone'}")

        elif kind == "ability":
            if isinstance(target_ref, str):
                match = ctx.find_ability(target_ref)
                if match is None:
                    print(f"Ability '{target_ref}' not found.")
                    return
                aid, ab = match
                users = [c.name for c in ctx.characters.values() if ab in c.abilities]
                print(f"[#{aid}] {ab.name} (power={ab.power}, cost={ab.cost}) | Users: {users or 'none'}")
            else:
                if not ctx.abilities:
                    print("No abilities yet.")
                for aid, ab in ctx.abilities.items():
                    users = [c.name for c in ctx.characters.values() if ab in c.abilities]
                    print(f"[#{aid}] {ab.name} (cost={ab.cost}) | Users: {users or 'none'}")

        else:
            print("Unknown category. Use: ls <char|item|ability>")

    registry.add_command("create", cmd_create, "create <char|item|ability>")
    registry.add_command("add", cmd_add, "add --char_id <id/name> --id <id/name>")
    registry.add_command("act", cmd_act, "act <attack|heal|ability> <actor> <target> [--id <id/name>]")
    registry.add_command("ls", cmd_ls, "ls <char|item|ability> [--id <id/name>]")