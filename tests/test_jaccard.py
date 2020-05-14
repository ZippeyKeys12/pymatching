from pytest_benchmark.fixture import BenchmarkFixture

from pymatching.jaccard import jaccard_distance, jaccard_index


def test_jaccard_index(benchmark: BenchmarkFixture):
    # Benchmarking
    benchmark(jaccard_index, 'Halloween', 'Black Christmas')

    # Correctness
    result = jaccard_index('Halloween', 'Black Christmas')
    assert '{:.10f}'.format(result) == '0.1111111111'


def test_jaccard_distance(benchmark: BenchmarkFixture):
    # Benchmarking
    benchmark(jaccard_distance, 'Halloween', 'Black Christmas')

    # Correctness
    result = jaccard_distance('Halloween', 'Black Christmas')
    assert '{:.10f}'.format(result) == '0.8888888889'
