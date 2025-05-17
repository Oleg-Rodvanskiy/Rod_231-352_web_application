import json

class Monster:
    def __init__(self, name, monster_type, weakness):
        self.name = name
        self.monster_type = monster_type
        self.weakness = weakness

    def to_dict(self):
        return {
            'name': self.name,
            'type': self.monster_type,
            'weakness': self.weakness
        }

class Bestiary:
    def __init__(self):
        self.monsters = {}

    def add_monster(self, name, monster_type, weakness):
        if name not in self.monsters:
            monster = Monster(name, monster_type, weakness)
            self.monsters[name] = monster
            print(f'Монстр "{name}" добавлен в бестиарий.')
        else:
            print(f'Монстр с именем "{name}" уже существует.')

    def remove_monster(self, name):
        if name in self.monsters:
            del self.monsters[name]
            print(f'Монстр "{name}" удален из бестиария.')
        else:
            print(f'Монстр с именем "{name}" не найден.')

    def search_by_weakness(self, weakness):
        found = [monster.to_dict() for monster in self.monsters.values() if monster.weakness.lower() == weakness.lower()]
        if not found:
            print(f'Монстры с уязвимостью к "{weakness}" не найдены.')
            return
        print(json.dumps(found, indent=4, ensure_ascii=False))

    def display_monsters(self):
        if not self.monsters:
            print('Бестиарий пуст.')
        else:
            for monster in self.monsters.values():
                print(f'Имя: {monster.name}, Тип: {monster.monster_type}, Слабость: {monster.weakness}')

def main():
    bestiary = Bestiary()

    while True:
        print("\nМеню:")
        print("1. Добавить монстра")
        print("2. Удалить монстра")
        print("3. Искать монстров по слабости")
        print("4. Показать всех монстров")
        print("5. Выйти")

        choice = input("Выберите действие (1-5): ")

        if choice == '1':
            name = input("Введите имя монстра: ")
            monster_type = input("Введите тип монстра: ")
            weakness = input("Введите слабость монстра: ")
            bestiary.add_monster(name, monster_type, weakness)

        elif choice == '2':
            name = input("Введите имя монстра для удаления: ")
            bestiary.remove_monster(name)

        elif choice == '3':
            weakness = input("Введите слабость для поиска (например, 'Серебро' или 'Игни'): ")
            bestiary.search_by_weakness(weakness)

        elif choice == '4':
            bestiary.display_monsters()

        elif choice == '5':
            print("Выход из программы.")
            break

        else:
            print("Неверный выбор. Пожалуйста, выберите число от 1 до 5.")

if __name__ == "__main__":
    main()