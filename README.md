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


----------------------------------------------------------------------------------------------------------------------------------------------------------------


## Практичне заняття 3. Наслідування та поліморфізм

### Пояснення архітектури та вибору структури

Структурований текст за своєю суттю є деревоподібною структурою даних, де елементи поділяються на дві категорії: **контейнери** (можуть містити вкладені елементи) та **кінцеві/листові елементи** (зберігають власний контент без нащадків).

* **Абстракція** задає єдиний контракт `render()` для всіх вузлів і виносить спільну логіку в базові абстрактні класи (`Container`, `Leaf`), щоб не дублювати код.
* **Наслідування** дозволяє спеціалізувати поведінку конкретних елементів (`Root`, `Heading`, `Paragraph`) від спільних предків.
* **Поліморфізм** дозволяє зберігати різні елементи в одній колекції (`list[TextElement]`) і викликати `render()` однаково незалежно від конкретного класу.

### Ролі ключових класів

* **`TextElement`** — абстрактний базовий клас (`ABC`), який визначає спільний інтерфейс усіх елементів структурованого тексту через метод `render() -> str`.
* **`Container`** — абстрактний клас контейнера: зберігає назву (`_name`), посилання на батька (`_parent`) та список дочірніх елементів (`_children`), реалізує додавання нащадків (`add_child`) і перевірку кореня (`is_root`).
* **`Leaf`** — абстрактний клас кінцевого елемента без дочірніх вузлів; зберігає вміст (`_content`) і безпечно приводить `None` до порожнього рядка.
* **`Root`** — кореневий контейнер документа (`parent=None`), виводить заголовок документа (`Title: ...`) і рендерить усіх нащадків.
* **`Heading`** — контейнер заголовка з рангом вкладеності (`rank >= 0`), формує табуляцію для самого заголовка та вкладених елементів.
* **`Paragraph`** — кінцевий текстовий блок, який повертає свій текст у `render()`.
* **`TextFactory`** — інкапсулює створення вузлів (`Root`, `Heading`, `Paragraph`) і навігацію по дереву (`_current`, методи `add_heading`, `add_paragraph`, `up`), спрощуючи побудову документа та майбутнє розширення форматів виводу.

### Діаграма класів

запуск: python -m text_system.main

```mermaid
classDiagram
    class TextElement {
        <<abstract>>
        +render()* str
    }

    class Container {
        <<abstract>>
        -_name : str
        -_parent : Container | None
        -_children : list~TextElement~
        +name() str
        +parent() Container | None
        +children() tuple~TextElement, ...~
        +add_child(child : TextElement) void
        +is_root() bool
        +render()* str
    }

    class Leaf {
        <<abstract>>
        -_content : str
        +content() str
        +render()* str
    }

    class Root {
        +render() str
    }

    class Heading {
        -_rank : int
        +rank() int
        +render() str
    }

    class Paragraph {
        +render() str
    }

    class TextFactory {
        -_root : Root
        -_current : Container
        +add_heading(name : str, rank : int) void
        +add_paragraph(content : str | None) void
        +up() void
        +render() str
        +__str__() str
    }

    TextElement <|-- Container : inherits
    TextElement <|-- Leaf : inherits
    Container <|-- Root : inherits
    Container <|-- Heading : inherits
    Leaf <|-- Paragraph : inherits
    Container o--> TextElement : _children (0..*)
    Container --> Container : _parent (0..1)
    TextFactory *-- Root : owns _root
    TextFactory --> Container : tracks _current
