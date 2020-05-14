import string
from itertools import combinations, permutations
from random import choice, seed
from typing import List

from pytest_benchmark.fixture import BenchmarkFixture

from pymatching.levenshtein import LevenshteinMetric
from pymatching.levenshtein import levenshtein_distance as ld
from pymatching.levenshtein import levenshtein_ratio as lr

from .util import random_word


def test_levenshtein_distance(benchmark: BenchmarkFixture):
    # Benchmarking
    result = benchmark(ld, 'A Nightmare on Elm Street', 'Friday the 13th')

    # Correctness
    assert result == 21


def test_levenshtein_ratio(benchmark: BenchmarkFixture):
    base = 'Friday the 13th'

    # Benchmarking
    benchmark(lr, 'A Nightmare on Elm Street', 'Friday the 13th')

    # Correctness
    seed('levenshtein_ratio')

    to_test: List[str] = []
    for l in range(2*len(base), 1):
        to_test.append(''.join(choice(string.ascii_lowercase)
                               for i in range(l)))

    distances = []
    results = []

    for t in to_test:
        distances.append((ld(t, base), t))

        # Subtract from 1 to flip order, prevents
        # testing issues with tied scores
        results.append((1 - lr(t, base), t))

    distances = sorted(distances)
    results = sorted(results)

    for i in range(len(to_test)):
        assert 0 <= results[i][0] <= 1
        assert results[i][-1] == distances[i][-1]


def test_levenshtein_metric():
    metric = LevenshteinMetric()

    # Test Metric Invariants
    seed(type(metric).__name__)
    for _ in range(100):
        test_set = [random_word(20), random_word(20), random_word(20)]

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
