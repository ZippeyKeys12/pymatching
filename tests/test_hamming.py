import string
from itertools import combinations, permutations
from random import choice, randint, seed
from typing import List

from pytest import raises
from pytest_benchmark.fixture import BenchmarkFixture

from pymatching.hamming import HammingMetric, hamming_distance, hamming_ratio

from .util import random_word


def test_hamming_distance(benchmark: BenchmarkFixture):
    # Benchmarking
    result = benchmark(hamming_distance, 'Friday the 69th', 'Friday the 13th')

    # Correctness
    assert result == 2

    # Errors
    with raises(ValueError):
        hamming_distance('A Nightmare on Elm Street', 'Friday the 13th')


def test_hamming_ratio(benchmark: BenchmarkFixture):
    base = 'Friday the 13th'

    # Benchmarking
    benchmark(hamming_distance, 'Friday the 69th', 'Friday the 13th')

    # Correctness
    seed('hamming')

    to_test: List[str] = []
    for l in range(100):
        copy = list(base)
        copy[randint(0, len(copy) - 1)] = choice(string.ascii_lowercase)
        to_test.append(''.join(copy))

    distances = []
    results = []

    for t in to_test:
        distances.append((hamming_distance(t, base), t))

        # Subtract from 1 to flip order, prevents
        # testing issues with tied scores
        results.append((1 - hamming_ratio(t, base), t))

    distances = sorted(distances)
    results = sorted(results)

    for i in range(len(to_test)):
        assert 0 <= results[i][0] <= 1
        assert results[i][-1] == distances[i][-1]

    # Errors
    with raises(ValueError):
        hamming_ratio('A Nightmare on Elm Street', 'Friday the 13th')


def test_hamming_metric():
    metric = HammingMetric()

    # Test Metric Invariants
    seed(type(metric).__name__)
    for _ in range(100):
        n = randint(1, 20)
        test_set = [random_word(n, n), random_word(n, n), random_word(n, n)]

        # Reflexivity
        for x in test_set:
            assert metric(x, x) == 0

        # Symmetry
        for x, y in combinations(test_set, 2):
            if x != y:
                assert metric(x, y) > 0

            assert metric(x, y) == metric(y, x)

        # Triangle Inequality
        for x, y, z in permutations(test_set, 3):
            assert metric(x, y) + metric(y, z) >= metric(x, z)
