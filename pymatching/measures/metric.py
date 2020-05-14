from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import Generic, List, Tuple, TypeVar, cast

T = TypeVar('T')


class Metric(Generic[T], metaclass=ABCMeta):
    """
    This abstract class exists for use in metric trees

    In order to be a metric the following
    properties must hold true:
    - metric(x, x) == 0
    - if x != y: metric(x, y) > 0
    - metric(x, y) == metrix(y, x)
    - metric(a, b) + metric(b, c) >= metric(a, c)
    """
    @abstractmethod
    def __call__(self, a: T, b: T) -> float:
        raise NotImplementedError()

    def __add__(self, other: Metric[T]) -> Metric[T]:
        if not isinstance(other, Metric):
            raise TypeError("other must a 'Metric'")

        metrics = []

        if isinstance(self, SumMetric):
            metrics.extend(self.metrics)
        else:
            metrics.append(self)

        if isinstance(other, SumMetric):
            metrics.extend(other.metrics)
        else:
            metrics.append(other)

        if all(map(lambda x: isinstance(x, ProductMetric), metrics)):
            return WeightedSumMetric(list(map(
                lambda x: (x.weight, x.metric),
                cast(List[ProductMetric], metrics))))

        return SumMetric(metrics)

    def __radd__(self, other: Metric[T]) -> Metric[T]:
        return self.__add__(other)

    def __mul__(self, other: float) -> ProductMetric[T]:
        if not isinstance(other, (int, float)):
            raise TypeError('other must scalar')

        weight = other

        if isinstance(self, ProductMetric):
            weight *= self.weight

        return ProductMetric(self, weight)

    def __rmul__(self, other: float) -> ProductMetric[T]:
        return self.__mul__(other)


class SumMetric(Metric[T]):
    __slots__ = ['metrics']

    def __init__(self, metrics: List[Metric[T]]):
        self.metrics = metrics

    def __call__(self, a: T, b: T) -> float:
        return sum(map(lambda x: x(a, b), self.metrics))


class ProductMetric(Metric[T]):
    __slots__ = ['metric', 'weight']

    def __init__(self, metric: Metric[T], weight: float):
        self.metric = metric
        self.weight = weight

    def __call__(self,  a: T, b: T) -> float:
        return self.weight * self.metric(a, b)


class WeightedSumMetric(Metric[T]):
    __slots__ = ['metrics']

    def __init__(self, metrics: List[Tuple[float, Metric[T]]]):
        self.metrics = metrics

    def __call__(self, a: T, b: T) -> float:
        return sum(map(lambda x: x[0] * x[1](a, b), self.metrics))
