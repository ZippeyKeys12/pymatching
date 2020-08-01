# pylint: disable-all
# flake8: noqa

__version__ = '0.0.1'

from .fuzzymatch import FuzzyMatchRatio, fuzzy_match, fuzzy_score
from .hamming import (HammingMetric, HammingRatio, hamming_distance,
                      hamming_ratio)
from .jaccard import jaccard_distance, jaccard_index
from .levenshtein import (LevenshteinMetric, LevenshteinRatio,
                          levenshtein_distance, levenshtein_ratio)
from .overlap import OverlapRatio, overlap_coefficient
from .sequencematch import (Sequence, SequenceMatcher, sequence_match_length,
                            sequence_match_ratio)
from .sorensendice import (Sequence, SorensenDiceRatio, SorensenRatio,
                           sorensen_coefficient, sorensen_dice_coefficient)
from .trie import Trie
from .word2vec import (Word2VecMetric, Word2VecRatio, word2vec_distance,
                       word2vec_similarity)
