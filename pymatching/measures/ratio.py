from __future__ import annotations

from abc import ABCMeta, abstractmethod
from functools import reduce
from typing import Generic, Iterable, List, Tuple, TypeVar, Union, cast

Number = Union[int, float]

T = TypeVar('T')


class Ratio(Generic[T], metaclass=ABCMeta):
    """
    This abstract class exists for use in comparisons
    """
    @abstractmethod
    def ratio_min(self) -> float:
        raise NotImplementedError()

    @abstractmethod
    def ratio_max(self) -> float:
        raise NotImplementedError()

    @abstractmethod
    def ratio(self, a: T, b: T) -> float:
        raise NotImplementedError()

    def normalized_ratio(self,  a: T, b: T) -> float:
        mi = self.ratio_min()
        ma = self.ratio_max()
        r = self.ratio(a, b)

        if 0 <= mi <= 1 and 0 <= ma <= 1:
            return r

        return (r - mi) / (ma - mi)

    def __add__(self, other: Union[Number, Ratio[T]]) -> Ratio[T]:
        valid_types = (int, float, Ratio)
        if not isinstance(other,  valid_types):
            raise TypeError(f"other must in {valid_types}")

        similarities: List[Ratio[T]] = []

        if isinstance(other, Ratio):
            if isinstance(other, SumRatio):
                similarities.extend(other.similarities)
            else:
                similarities.append(other)

            return SumRatio(similarities)

        else:
            other = cast(float, other)

            if isinstance(self, SAddRatio):
                return SAddRatio(
                    self.similarity, self.scalar + other)
            else:
                return SAddRatio(self, other)

    def __radd__(self, other: Ratio[T]) -> Ratio[T]:
        return self.__add__(other)

    def __mul__(self, other: Union[Number, Ratio[T]]) -> Ratio[T]:
        valid_types = (int, float, Ratio)
        if not isinstance(other,  valid_types):
            raise TypeError(f"other must in {valid_types}")

        similarities: List[Ratio[T]] = []

        if isinstance(self, ProductRatio):
            similarities.extend(self.similarities)
        else:
            similarities.append(self)

        if isinstance(other, Ratio):
            if isinstance(other, ProductRatio):
                similarities.extend(other.similarities)
            else:
                similarities.append(other)

            return ProductRatio(similarities)

        else:
            other = cast(float, other)

            if isinstance(self, SMulRatio):
                return SMulRatio(
                    self.similarity, self.scalar * other)
            else:
                return SMulRatio(self, other)

    def __rmul__(self, other: Ratio[T]) -> Ratio[T]:
        return self.__mul__(other)


class SAddRatio(Ratio[T]):
    __slots__ = ['_min', '_max', 'scalar', 'similarity']

    def __init__(self, similarity: Ratio[T], scalar: float):
        self.similarity = similarity
        self.scalar = scalar
        self._min = scalar + similarity.ratio_min()
        self._max = scalar + similarity.ratio_max()

    def ratio_min(self) -> float:
        return self._min

    def ratio_max(self) -> float:
        return self._max

    def ratio(self,  a: T, b: T) -> float:
        return self.scalar + self.similarity.ratio(a, b)


class SumRatio(Ratio[T]):
    __slots__ = ['_min', '_max', 'similarities']

    def __init__(self, similarities: Iterable[Ratio[T]]):
        self.similarities = similarities
        self._min = sum(map(lambda x: x.ratio_min(), similarities))
        self._max = sum(map(lambda x: x.ratio_max(), similarities))

    def ratio_min(self) -> float:
        return self._min

    def ratio_max(self) -> float:
        return self._max

    def ratio(self,  a: T, b: T) -> float:
        return sum(map(lambda x: x.ratio(a, b), self.similarities))


class SMulRatio(Ratio[T]):
    __slots__ = ['_min', '_max', 'scalar', 'similarity']

    def __init__(self, similarity: Ratio[T], scalar: float):
        self.similarity = similarity
        self.scalar = scalar
        self._min = scalar * similarity.ratio_min()
        self._max = scalar * similarity.ratio_max()

    def ratio_min(self) -> float:
        return self._min

    def ratio_max(self) -> float:
        return self._max

    def ratio(self,  a: T, b: T) -> float:
        return self.scalar * self.similarity.ratio(a, b)


class ProductRatio(Ratio[T]):
    __slots__ = ['_min', '_max', 'similarities']

    def __init__(self, similarities: Iterable[Ratio[T]]):
        self.similarities = similarities
        self._min = reduce(float.__mul__, map(
            lambda x: x.ratio_min(), similarities))
        self._max = reduce(float.__mul__, map(
            lambda x: x.ratio_max(), similarities))

    def ratio_min(self) -> float:
        return self._min

    def ratio_max(self) -> float:
        return self._max

    def ratio(self, a: T, b: T) -> float:
        return reduce(float.__mul__, map(lambda x: x.ratio(a, b), self.similarities))


class WeightedSumRatio(Ratio[T]):
    __slots__ = ['_min', '_max', 'similarities']

    def __init__(self, similarities: Iterable[Tuple[float, Ratio[T]]]):
        self.similarities = similarities
        self._min = sum(map(lambda x: x[0] * x[1].ratio_min(), similarities))
        self._max = sum(map(lambda x: x[0] * x[1].ratio_max(), similarities))

    def ratio_min(self) -> float:
        return self._min

    def ratio_max(self) -> float:
        return self._max

    def ratio(self,  a: T, b: T) -> float:
        return sum(map(lambda x: x[0] * x[1].ratio(a, b), self.similarities))
