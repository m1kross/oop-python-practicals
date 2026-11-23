"""CLI commands for the Structured Text system."""

from cli.engine import CommandRegistry
from cli.parser import ParsedCommand
from text_system.factory import TextFactory, TextType


def register_text_commands(registry: CommandRegistry, factory: TextFactory) -> None:
    """Register Text CLI commands into the registry."""

    def cmd_pwd(_: ParsedCommand) -> None:
        print(factory.pwd())

    def cmd_print(cmd: ParsedCommand) -> None:
        whole = bool(cmd.options.get("whole", False))
        show_id = bool(cmd.options.get("id", False))
        print(factory.render(whole=whole, show_id=show_id))

    def cmd_add(cmd: ParsedCommand) -> None:
        if len(cmd.args) < 2:
            print("Usage: add <container|leaf> <type>  (e.g., add container heading | add leaf paragraph)")
            return
        category, elem_type = cmd.args[0].lower(), cmd.args[1].lower()

        if category == "container" and elem_type == TextType.HEADING.value:
            title = input("Heading title: ").strip()
            if not title:
                print("Heading title cannot be empty.")
                return
            rank_raw = input("Rank (leave empty for auto): ").strip()
            rank = int(rank_raw) if rank_raw else None
            node = factory.add_container(TextType.HEADING, name=title, rank=rank)
            print(f"Added heading [#{node.element_id}] '{title}'. Current path: {factory.pwd()}")

        elif category == "leaf" and elem_type == TextType.PARAGRAPH.value:
            content = input("Paragraph text: ")
            node = factory.add_leaf(TextType.PARAGRAPH, content=content)
            print(f"Added paragraph [#{node.element_id}].")

        else:
            print("Unsupported combination. Use: add container heading | add leaf paragraph")

    def cmd_rm(cmd: ParsedCommand) -> None:
        elem_name = cmd.args[0] if cmd.args else None
        target_label = f"'{elem_name}'" if elem_name else f"current container '{factory.current.name}'"
        confirm = input(f"Remove {target_label}? (y/n): ").strip().lower()
        if confirm not in ("y", "yes"):
            print("Cancelled.")
            return

        removed = factory.remove(elem_name)
        if removed is None:
            print("Nothing removed (element not found or cannot remove Root).")
        else:
            print(f"Removed '{removed}'. Current path: {factory.pwd()}")

    def cmd_up(_: ParsedCommand) -> None:
        if factory.up():
            print(f"Moved up to: {factory.pwd()}")
        else:
            print("Already at root (/).")

    def cmd_cd(cmd: ParsedCommand) -> None:
        id_opt = cmd.options.get("id")
        if isinstance(id_opt, str) and id_opt.isdigit():
            if factory.cd_by_id(int(id_opt)):
                print(f"Moved to: {factory.pwd()}")
            else:
                print(f"Container with id {id_opt} not found.")
            return

        if not cmd.args:
            print("Usage: cd <path> | cd --id <container_id>")
            return

        if factory.cd(cmd.args[0]):
            print(f"Moved to: {factory.pwd()}")
        else:
            print(f"Path '{cmd.args[0]}' not found.")

    registry.add_command("pwd", cmd_pwd, "Show current document path")
    registry.add_command("print", cmd_print, "print [--whole] [--id]")
    registry.add_command("add", cmd_add, "add <container|leaf> <type>")
    registry.add_command("rm", cmd_rm, "rm [<elem_name>]")
    registry.add_command("up", cmd_up, "Move to parent container")
    registry.add_command("cd", cmd_cd, "cd <path> | cd --id <container_id>")