from typing import Collection, TypeVar

from .measures import Metric, Ratio

T = TypeVar('T')


def hamming_distance(a: Collection[T], b: Collection[T]) -> int:
    if len(a) != len(b):
        raise ValueError("'a' and 'b' must be of equal length")

    return sum(x != y for x, y in zip(a, b))


def hamming_ratio(a: Collection[T], b: Collection[T]) -> float:
    if len(a) != len(b):
        raise ValueError("'a' and 'b' must be of equal length")

    return 1 - hamming_distance(a, b) / len(a)


class HammingMetric(Metric[Collection[T]]):
    def __call__(self, a: Collection[T], b: Collection[T]) -> int:
        return hamming_distance(a, b)


class HammingRatio(Ratio):
    def ratio_min(self) -> int:
        return 1

    def ratio_max(self) -> int:
        return 0

    def ratio(self, a: Collection[T], b: Collection[T]) -> float:
        return hamming_ratio(a, b)
