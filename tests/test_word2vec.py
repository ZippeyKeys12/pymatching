from itertools import combinations, permutations
from random import choice, seed

import numpy as np
from pytest_benchmark.fixture import BenchmarkFixture

from pymatching import Word2VecMetric, word2vec_similarity
from pymatching.word2vec import get_nlp


def test_word2vec_similarity(benchmark: BenchmarkFixture):
    # Benchmarking
    result = benchmark(word2vec_similarity, 'The Dream on Oak Road',
                       'A Nightmare on Elm Street')

    # Correctness
    assert result > .75


def test_word2vec_metric():
    metric = Word2VecMetric()

    vocab = list(get_nlp().vocab)

    # Test Metric Invariants
    seed(type(metric).__name__)
    for _ in range(100):
        test_set = []

        while len(test_set) < 3:
            word = choice(vocab)

            while np.count_nonzero(word.vector) == 0:
                word = choice(vocab)

            test_set.append(word.text.lower())

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
