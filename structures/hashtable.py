import json
from rich.console import Console
from datetime import datetime

console = Console()


class MyHashTable:
    __DELETED = object()

    def __init__(self):
        self.__capacity = 11
        self.__size = 0
        self.__table = [None] * self.__capacity
        self.__is_rehashing = False

    def __len__(self):
        return self.__size

    def __index(self, i, key):
        hash_1 = hash(key) % self.__capacity
        hash_2 = 1 + (hash(key) % (self.__capacity - 1))
        index = (hash_1 + i * hash_2) % self.__capacity
        return index

    def __getitem__(self, key):
        i = 0
        while i < self.__capacity:
            index = self.__index(i, key)
            item = self.__table[index]

            if item is None:
                break
            if item is not self.__DELETED and item[0] == key:
                return item[1]

            i += 1
        raise KeyError(f'Invalid key: {key}')

    def __setitem__(self, key, value):
        load_factor = self.__size / self.__capacity
        potential_index = None

        if load_factor > 0.7:
            self.__rehash()

        i = 0
        while True:
            index = self.__index(i, key)
            item = self.__table[index]

            if item is None:
                # empty item
                index = potential_index if potential_index is not None else index
                self.__size += 1
                break
            elif item is self.__DELETED and potential_index is None:
                # first encounter of removed item
                potential_index = index
            elif item[0] == key:
                # exact key item
                break

            i += 1

            if i < self.__capacity:
                pass
            elif potential_index is not None:
                index = potential_index
                self.__size += 1
                break
            else:
                # rehash to avoid infinite loop and start over
                self.__rehash()
                potential_index = None
                i = 0

        self.__table[index] = (key, value)

        if not self.__is_rehashing:
            self.__log(key)

    def __str__(self):
        if self.__size == 0:
            return 'HashTable is empty'

        items_str = []

        for item in self.__table:
            if item and item is not self.__DELETED:
                items_str.append(str(item))

        result = '{ ' + ', '.join(items_str) + ' }'
        return result

    def put(self, key, value):
        self.__setitem__(key, value)

    def get(self, key):
        return self.__getitem__(key)

    def __rehash(self):
        self.__is_rehashing = True
        old_table = self.__table

        self.__capacity = self.__capacity * 2 + 1
        self.__table = [None] * self.__capacity
        self.__size = 0

        for item in old_table:
            if item and item is not self.__DELETED:
                self.__setitem__(item[0], item[1])

        self.__is_rehashing = False

    @property
    def capacity(self):
        return self.__capacity

    def remove(self, key):
        if self.__size == 0:
            return

        i = 0
        while i < self.__capacity:

            index = self.__index(i, key)
            item = self.__table[index]

            if item is None:
                break
            if item is not self.__DELETED and item[0] == key:
                self.__table[index] = self.__DELETED
                self.__size -= 1
                return

            i += 1
        raise KeyError(f'Invalid key: {key}')

    def __iter__(self):
        for item in self.__table:
            if item and item is not self.__DELETED:
                yield item[0]

    def items(self):
        for item in self.__table:
            if item and item is not self.__DELETED:
                yield item

    def save_to_json(self, filename='hashtable.json'):
        data = [{"key": k1, "value": v1} for k1, v1 in self.items()]

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f)
                console.print(f"File '{filename}' saved!", style='green')
        except Exception as e:
            console.print(f"[{e.__class__.__name__}] '{filename}': {e}", style='red')

    def load_from_json(self, filename='hashtable.json'):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self.__init__()

            for item in data:
                self.put(item['key'], item['value'])
        except FileNotFoundError:
            console.print(f"File '{filename}' was not found!", style='red')
        except json.JSONDecodeError:
            console.print(f"Corrupted file '{filename}'!", style='red')

        except Exception as e:
            console.print(f"[{e.__class__.__name__}] '{filename}': {e}", style='red')

    def __log(self, key):
        filename = 'history.log'

        try:
            with open(filename, 'a', encoding='utf-8') as f:
                time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                f.write(f'[{time}] Додано елемент: Ключ={key}\n')
        except Exception as e:
            console.print(f"[{e.__class__.__name__}] '{filename}': {e}", style='red')
