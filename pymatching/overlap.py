from typing import Iterable, TypeVar

from .measures import Ratio

T = TypeVar('T')


def overlap_coefficient(one: Iterable[T], two: Iterable[T]) -> float:
    a = set(one)
    b = set(two)

    return len(a & b) / min(len(a), len(b))


class OverlapRatio(Ratio):
    def ratio_min(self) -> int:
        return 0

    def ratio_max(self) -> int:
        return 1

    def ratio(self, a: Iterable[T], b: Iterable[T]) -> float:
        return overlap_coefficient(a, b)
