from typing import Iterable, TypeVar

T = TypeVar('T')


def jaccard_index(one: Iterable[T], two: Iterable[T]) -> float:
    a = set(one)
    b = set(two)

    len_inter = len(a & b)

    return len_inter / (len(a) + len(b) - len_inter)


def jaccard_distance(one: Iterable[T], two: Iterable[T]) -> float:
    return 1 - jaccard_index(one, two)
