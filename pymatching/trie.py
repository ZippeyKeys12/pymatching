from typing import Callable, Dict, Generic, Iterable, List, TypeVar

T = TypeVar('T')


class TrieNode(Generic[T]):
    def __init__(self, value: T, is_root: bool = False):
        self.value = value
        self.children: Dict[T, TrieNode[T]] = {}
        self.is_complete = False
        self.is_root = is_root

    def get_paths(self, all_paths: bool = False) -> List[List[T]]:
        paths = []

        if not self.is_root:
            if not all_paths and self.is_complete:
                paths.append([self.value])

            for child in self.children.values():
                for comp in child.get_paths():
                    paths.append([self.value] + comp)

        else:
            for child in self.children.values():
                for comp in child.get_paths():
                    paths.append(comp)

        return paths


class Trie(Generic[T]):
    __slots__ = ['empty', 'root', 'merger', 'size']

    def __init__(self, empty: Iterable[T], merger: Callable[[Iterable[T]], Iterable[T]] = lambda x: x):
        self.empty = empty
        self.root = TrieNode[T]('ROOT', is_root=True)  # type:ignore
        self.merger = merger
        self.size = 0

    def add(self, new_value: Iterable[T]):
        curr = self.root

        for val in new_value:
            if val not in curr.children:
                self.size += 1
                curr.children[val] = TrieNode(val)

            curr = curr.children[val]

        curr.is_complete = True

    def get_children(self, item: Iterable[T]) -> Dict[T, TrieNode[T]]:
        curr = self.root

        for val in item:
            if val in curr.children:
                curr = curr.children[val]

            else:
                raise KeyError(f'{item}')

        return curr.children

    def get_completions(self, prefix: Iterable[T] = []) -> List[Iterable[T]]:
        curr = self.root

        path = []

        for val in prefix:
            path.append(val)

            if val in curr.children:
                curr = curr.children[val]

            else:
                raise KeyError(f'{prefix}')

        return [self.merger(path[:-1] + x) for x in curr.get_paths()]

    def get_paths(self, prefix: Iterable[T] = []) -> List[Iterable[T]]:
        curr = self.root

        path = []

        for val in prefix:
            path.append(val)

            if val in curr.children:
                curr = curr.children[val]

            else:
                raise KeyError(f'{prefix}')

        return [self.merger(path[:-1] + x) for x in curr.get_paths(all_paths=True)]

    def __contains__(self, item: Iterable[T]) -> bool:
        curr = self.root

        for val in item:
            if val in curr.children:
                curr = curr.children[val]

            else:
                return False

        return curr.is_complete

    def __getitem__(self, prefix: Iterable[T]) -> List[Iterable[T]]:
        return self.get_completions(prefix)

    def __len__(self) -> int:
        return self.size
