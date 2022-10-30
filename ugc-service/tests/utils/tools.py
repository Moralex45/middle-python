import random
import string


def get_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def get_random_int(start: int = 0, end: int = 1000000) -> int:
    return random.randint(start, end)
