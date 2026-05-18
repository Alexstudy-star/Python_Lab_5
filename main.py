from rich.console import Console

console = Console()

# task 1
print('--- task 1 ---')

console.print('Initialize test: import modules!', style='yellow')
try:
    from structures import MyHashTable, BinarySearchTree
    console.print(f'Successfully imported!', style='green')
except ImportError as e:
    console.print(f'[ImportError]: {e}', style='red')


console.print('Initialize test: create class instance!', style='yellow')
try:
    hash_table = MyHashTable()
    console.print(f'Successfully created {hash_table.__class__.__name__} instance!', style='green')
except Exception as e:
    console.print(f'[{e.__class__.__name__}]: {e}', style='red')


console.print('Initialize test: search by key!', style='yellow')
try:
    table = MyHashTable()
    value = table['apple']
    console.print(f'Success: value = {value} !', style='green')
except Exception as e:
    console.print(f'[{e.__class__.__name__}]: {e}', style='red')

# task 2
print('\n--- task 2 ---')
ht = MyHashTable()
ht.put('Hello', 'World')
console.print(f'Table: {ht}', style='green')

ht.save_to_json()

new_ht = MyHashTable()
new_ht.load_from_json()
console.print(f'Loaded table: {new_ht}', style='green')

new_ht.load_from_json("missing_file")
