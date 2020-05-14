from typing import Sequence, TypeVar

from .measures import Ratio

T = TypeVar('T')


def sorensen_dice_coefficient(one: Sequence[T], two: Sequence[T]) -> float:
    x = set(one)
    y = set(two)

    return 2 * len(x & y) / (len(x) + len(y))


dice_coefficient = sorensen_dice_coefficient
sorensen_coefficient = sorensen_dice_coefficient


class SorensenDiceRatio(Ratio[Sequence[T]]):
    def ratio_min(self):
        return 0

    def ratio_max(self):
        return 1

    def ratio(self, a: Sequence[T], b: Sequence[T]) -> float:
        return sorensen_coefficient(a, b)


DiceRatio = SorensenDiceRatio
SorensenRatio = SorensenDiceRatio
