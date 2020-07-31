from itertools import combinations
from math import ceil
from random import sample, seed
from typing import List, Tuple

import pytest
from pytest_benchmark.fixture import BenchmarkFixture

from pymatching.fuzzymatch import fuzzy_match, fuzzy_score


@pytest.mark.parametrize("inputs,results", [
    # Single word
    (
        ('God', 'The Godfather'),
        (['God'], 'God', 4)
    ),

    # Multi-word
    (
        ('ANime', 'A Nightmare on Elm Street'),
        (['A', 'Ni', 'm', 'e'], 'A Nightmare', 0)
    ),

    # Until end of word
    (
        ('Thing', 'The Shining'),
        (['Th', 'ing'], 'The Shining', 0)
    ),

    # Not Found
    (
        ('Q', 'The Living Daylights'),
        ([], '', -1)
    ),

    # Other Special Cases
    (
        ('Th', 'ThTh'),
        (['Th'], 'Th', 0)
    ),
    (
        ('Thing', 'Thing Th i n g'),
        (['Thing'], 'Thing', 0)
    ),
    (
        ('Thing', 'T hi hin ng g'),
        (['T', 'hin', 'g'], 'T hi hin ng', 0)
    )
])
def test_fuzzy_match(inputs: Tuple[str, str], results: Tuple[List[str], str], benchmark: BenchmarkFixture):
    # Benchmarking
    result = benchmark(fuzzy_match, *inputs)

    # Correctness
    assert result == results


def test_fuzzy_score(benchmark: BenchmarkFixture):
    # Benchmarking
    benchmark(fuzzy_score, 'ANime', 'A Nightmare on Elm Street')
