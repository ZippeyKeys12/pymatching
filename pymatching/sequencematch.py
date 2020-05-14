from difflib import SequenceMatcher
from typing import Sequence, TypeVar

T = TypeVar('T')


def sequence_match_length(one: Sequence[T], two: Sequence[T]) -> int:
    matcher = SequenceMatcher(None, one, two)

    return sum(triple[-1] for triple in matcher.get_matching_blocks())


def sequence_match_ratio(one: Sequence[T], two: Sequence[T]) -> float:
    return 2 * sequence_match_length(one, two) / (len(one) + len(two))
