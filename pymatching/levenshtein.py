from typing import Sequence, TypeVar

import numba
import numpy as np

from .measures import Metric, Ratio

T = TypeVar('T')


@numba.jit(cache=True)
def levenshtein_distance(one: Sequence[T], two: Sequence[T]) -> int:
    l1 = len(one) + 1
    l2 = len(two) + 1

    distances = np.zeros((l1, l2))

    for i in range(l1):
        distances[i][0] = i

    for i in range(l2):
        distances[0][i] = i

    for i in range(1, l1):
        for j in range(1, l2):
            if (one[i - 1] == two[j - 1]):
                distances[i][j] = distances[i - 1][j - 1]

            else:
                distances[i][j] = 1 + min(
                    distances[i][j - 1],
                    distances[i - 1][j],
                    distances[i - 1][j - 1]
                )

    return distances[l1 - 1][l2 - 1]


@numba.jit()
def levenshtein_ratio(one: Sequence[T], two: Sequence[T]) -> float:
    return 1 - levenshtein_distance(one, two) / max(len(one), len(two))


class LevenshteinMetric(Metric[Sequence[T]]):
    def __call__(self, a: Sequence[T], b: Sequence[T]) -> int:
        return levenshtein_distance(a, b)


class LevenshteinRatio(Ratio[Sequence[T]]):
    def ratio_min(self) -> int:
        return 1

    def ratio_max(self) -> int:
        return 0

    def ratio(self, a: Sequence[T], b: Sequence[T]) -> float:
        return levenshtein_ratio(a, b)
