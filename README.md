# Практичне заняття 2. Інкапсуляція — UML-діаграма класів

```mermaid
classDiagram
    class Logger {
        -bool _enabled
        +bool enabled
        +log(message: str) None
    }

    class Ability {
        -str _name
        -int _power
        -int _cost
        +str name
        +int power
        +int cost
    }

    class Character {
        -str _name
        -int _max_hp
        -int _hp
        -int _attack
        -int _armor
        -int _penetration
        -int _energy
        -list~Ability~ _abilities
        -Logger _logger
        +str name
        +int hp
        +bool is_alive
        +int attack
        +int armor
        +int penetration
        +int energy
        +tuple~Ability~ abilities
        +add_ability(ability: Ability) None
        +spend_energy(amount: int) bool
        +restore_energy(amount: int) None
        +calculate_incoming_damage(raw_damage: int, attacker_penetration: int) int
        +take_damage(raw_damage: int, attacker_penetration: int) int
    }

    class Game {
        -Logger _logger
        -int _turn
        +int turn
        +basic_attack(attacker: Character, target: Character) int
        +use_ability(actor: Character, ability: Ability, target: Character) int
    }

    Character "0..*" o-- "0..*" Ability : aggregates
    Character --> "1" Logger : uses
    Game --> "1" Logger : uses
    Game --> "0..*" Character : orchestrates
    Game ..> Ability : uses
```

## Ролі класів та взаємодія

- **`Logger`** — інкапсулює вивід повідомлень про події (побічний ефект). Дозволяє вимкнути або змінити спосіб логування без зміни бізнес-логіки `Character` та `Game`.
- **`Ability`** — описує здібність персонажа (`name`, `power`, `cost`) і захищає свої поля від некоректних значень через `@property`.
- **`Character`** — зберігає стан персонажа (`_hp`, `_energy`, `_armor`, `_penetration`, `_attack`) та інкапсулює правила отримання шкоди (`take_damage`, `calculate_incoming_damage`).
- **`Game`** — керує ходом бою (`_turn`), перевіряє можливість атаки або використання здібності, списує енергію та координує взаємодію між персонажами і `Logger`.
