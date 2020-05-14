from pytest_benchmark.fixture import BenchmarkFixture

from pymatching.sorensendice import sorensen_dice_coefficient


def test_sorensen_dice_coefficient(benchmark: BenchmarkFixture):
    # Benchmarking
    benchmark(sorensen_dice_coefficient, 'Halloween', 'Black Christmas')

    # Correctness
    result = sorensen_dice_coefficient('Halloween', 'Black Christmas')
    assert '{:.10f}'.format(result) == '0.2000000000'
