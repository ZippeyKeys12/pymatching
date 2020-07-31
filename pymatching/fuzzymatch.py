import re
from functools import lru_cache
from math import ceil
from typing import List, Tuple

import numba

from.measures.ratio import Ratio


def _remaining(final_match: List[int]) -> int:
    return len(list(filter(lambda x: x == -1, final_match)))


def _spread_consec(matches, final_match):
    final_match = final_match.copy()

    oleft = len(matches)
    left = _remaining(final_match)
    while left < oleft and final_match.count(-1) > 0:
        for i, l in list(enumerate(matches))[final_match.index(-1):]:
            if final_match[i] == -1:
                try:
                    bot = final_match[i - 1]
                    if bot > -1 and (bot + 1) in l:
                        final_match[i] = bot + 1

                except (IndexError, TypeError):
                    pass

                try:
                    top = final_match[i + 1]
                    if top > -1 and (top - 1) in l:
                        final_match[i] = top - 1

                except (IndexError, TypeError):
                    pass

        oleft = left
        left = _remaining(final_match)

    return final_match


def _capture(s: str, l: List[int]) -> str:
    return s[l[0]:l[-1] + 1]


def _compress_match(text: str, match: List[int]) -> Tuple[List[str], str, int]:
    parts: List[str] = []

    # Finds consecutive matches
    res: List[int] = []
    last = match[0]
    for m in match:
        if m - last > 1:
            parts.append(_capture(text, res))
            res = []
        res.append(m)
        last = m
    parts.append(_capture(text, res))

    return (parts, text[match[0]: match[-1] + 1], match[0])


def fuzzy_match(pattern: str, text: str) -> Tuple[List[str], str, int]:
    def patlist(pat, sep):
        return '(?=({}))'.format(sep.join(list(map(lambda x: '({})'.format(re.escape(x)), pat))))

    # Mark all viable character indices
    matches: List[List[int]] = [[] for _ in range(len(pattern))]
    for s in range(len(pattern)):
        pat = patlist(pattern[s:], '.*')

        if s == 0:
            ttext = text
            st = -1
        else:
            # If previous character index list was empty, abort
            if len(matches[s - 1]) == 0:
                return ([], '', -1)

            # Else make string with remaining valid text
            st = matches[s - 1][0]
            ttext = ' ' * (st + 1) + text[st + 1:]

        m = re.search(pat, ttext)
        while m is not None and m.start(1) > st:
            st = m.start(1)
            matches[s].append(st)

            ttext = ' ' * (st + 1) + text[st + 1:]

            m = re.search(pat, ttext)

        # if s == 0:
        #     matches[s] = [matches[s][-1]]
        # elif s == len(pattern) - 1:
        #     matches[s] = [matches[s][0]]

    # If last character index list is empty, abort
    if len(matches[-1]) == 0:
        return ([], '', -1)

    # -1 marks undecided indices
    final_match: List[int] = [-1 for _ in range(len(pattern))]

    # For any characters with only one choice, fill in index
    for i, l in enumerate(matches[1: -1]):
        if len(l) == 1:
            final_match[i + 1] = l[0]

    # Propagate decided indices to form groups
    final_match = _spread_consec(matches, final_match)

    # If there are remaining characters that aren't part of an existing group
    while _remaining(final_match) != 0:
        i = final_match.index(-1)

        # If character is part of neighboring groups, then index doesn't matter
        for j in range(1, len(final_match) - 1):
            if final_match[j - 1] != -1 and final_match[j] == -1 and final_match[j + 1] != -1:
                final_match[j] = matches[j][0]

        # Else, find the index that has the largest group
        smallest = (_remaining(final_match), final_match)
        for j in matches[i]:
            fm = final_match.copy()
            fm[i] = j

            fm = _spread_consec(matches, fm)
            s = _remaining(fm)

            if smallest is None or s < smallest[0]:
                smallest = (s, fm)

        final_match = smallest[1]

    # Put the corresponding strings
    return _compress_match(text, final_match)
