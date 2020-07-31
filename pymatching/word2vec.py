import numpy as np
import spacy

from .measures import Metric, Ratio

spacy.prefer_gpu()
nlp = spacy.load("en_core_web_md")


def word2vec_distance(one: str, two: str) -> float:
    # if one.split() != 1:
    #     raise ValueError("'one' must be a single word")

    # if two.split() != 1:
    #     raise ValueError("'two' must be a single word")

    return np.linalg.norm(nlp(one).vector - nlp(two).vector)


def word2vec_similarity(one: str, two: str) -> float:
    a = nlp(one)
    b = nlp(two)

    if np.count_nonzero(a.vector) == 0:
        return 0

    if np.count_nonzero(b.vector) == 0:
        return 0

    return a.similarity(b)


class Word2VecMetric(Metric[str]):
    def __call__(self, a: str, b: str) -> float:
        return word2vec_distance(a, b)


class Word2VecRatio(Ratio[str]):
    def ratio_min(self) -> int:
        return 1

    def ratio_max(self) -> int:
        return 0

    def ratio(self, a: str, b: str) -> float:
        return word2vec_similarity(a, b)
