class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None

    def __str__(self):
        return f'({self.key}, {self.value})'


class BinarySearchTree:
    def __init__(self):
        self._root = None
        self._size = 0

    def insert(self, key, value):
        self._root = self._insert(self._root, key, value)

    def _insert(self, node, key, value):
        if node is None:
            self._size += 1
            return Node(key, value)

        if key == node.key:
            node.value = value
        elif key < node.key:
            node.left = self._insert(node.left, key, value)
        else:
            node.right = self._insert(node.right, key, value)
        return node

    def search(self, key):
        return self._search(self._root, key)

    def _search(self, node, key):
        if node is None:
            raise KeyError(f'Invalid key: {key}')

        if key == node.key:
            return node.value
        elif key < node.key:
            return self._search(node.left, key)
        else:
            return self._search(node.right, key)

    def find_min(self):
        if self._root is None:
            return None

        return self._find_min(self._root)

    def _find_min(self, node):
        if node.left:
            return self._find_min(node.left)
        else:
            return node

    def find_max(self):
        if self._root is None:
            return None

        return self._find_max(self._root)

    def _find_max(self, node):
        if node.right:
            return self._find_max(node.right)
        else:
            return node

    def inorder_traversal(self):
        yield from self._in_order(self._root)

    def _in_order(self, node):
        if node:
            yield from self._in_order(node.left)
            yield (node.key, node.value)
            yield from self._in_order(node.right)

    def get_height(self):
        return self._get_height(self._root)

    def _get_height(self, node):
        if not node:
            return 0

        left_height = self._get_height(node.left)
        right_height = self._get_height(node.right)

        return 1 + max(left_height, right_height)

    def find_range(self, min_key, max_key):
        return self._find_range(self._root, min_key, max_key)

    def _find_range(self, node, min_key, max_key):
        if not node:
            return []

        result = []

        if node.key > min_key:
            left = self._find_range(node.left, min_key, max_key)
            result += left

        if min_key <= node.key <= max_key:
            result += [node.value]

        if node.key < max_key:
            right = self._find_range(node.right, min_key, max_key)
            result += right

        return result
