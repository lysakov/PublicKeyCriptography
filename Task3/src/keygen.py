from utils import *
from math import log, floor

class KeyGenerator(object):

    def get_key(self, n : int) -> tuple:
        p = get_random_prime(n)
        g = get_primitive_root(p)
        y = randint(1, p - 1)

        return (y, g, p)

    def get_vulnerable_pohlig_hellman_key(self, n : int, smoothness = 2**8) -> tuple:
        p1 = 2

        while not is_prime(p1 + 1) or p1 == 2:
            p1 = 1
            while p1.bit_length() < n:
                deg = randint(1, 5)
                devider = randint(1, smoothness)**deg
                p1 *= devider

        return randint(1, p1), get_primitive_root(p1 + 1), p1 + 1