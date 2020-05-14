import string
from random import choice, randint
from typing import Optional


def random_word(a: int, b: Optional[int] = None) -> str:
    if b is None:
        mi = 1
        ma = a
    else:
        mi = a
        ma = b

    return ''.join(choice(string.ascii_letters) for _ in range(randint(mi, ma)))
