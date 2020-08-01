from itertools import combinations
from random import sample, seed
from typing import List

from pytest_benchmark.fixture import BenchmarkFixture

from pymatching import sequence_match_length, sequence_match_ratio


def test_sequence_match_length(benchmark: BenchmarkFixture):
    base = 'A Nightmare on Elm Street'

    # Benchmarking
    benchmark(sequence_match_length, 'ANime', 'A Nightmare on Elm Street')

    # Correctness
    assert sequence_match_length('ANime', 'A Nightmare on Elm Street') == 5

    to_test: List[str] = []

    for i in range(1, len(base)):
        to_test.extend(map(''.join, combinations(base, i)))

    seed('sequence_match_length')
    to_test = sample(to_test, 10)

    for t in to_test:
        assert sequence_match_length(t, base) == len(t)


def test_sequence_match_ratio(benchmark: BenchmarkFixture):
    base = 'A Nightmare on Elm Street'

    # Benchmarking
    benchmark(sequence_match_ratio, 'ANime', base)

    # Correctness
    to_test: List[str] = []

    for i in range(1, len(base)):
        to_test.extend(map(''.join, combinations(base, i)))

    seed('sequence_match_ratio')
    to_test = sample(to_test, 10)

    for t in to_test:
        assert 0 <= sequence_match_ratio(t, base) <= 1
