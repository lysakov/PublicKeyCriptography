from utils import *

from random import randint
from decimal import Decimal

import math

class KeyGen(object):

    def get_weak_wiener_keys(self, n):
        p, q = get_random_prime(n), get_random_prime(n)
        d = 0
        while math.gcd(d, (p - 1)*(q - 1)) != 1:
            d = randint(0, int(Decimal(1/3) * Decimal(p*q)**Decimal(1/4)))
        e = pow(d, -1, (p - 1)*(q - 1))

        return (d, e, p*q)

    def get_weak_low_exponent_key(self, n):
        p, q = get_random_prime(n), get_random_prime(n)
        e = 0
        while math.gcd(e, (p - 1)*(q - 1)) != 1:
            e = randint(0, 2*n)
        d = pow(e, -1, (p - 1)*(q - 1))

        return (d, e, p*q)

    def get_weak_cycle_key(self, n):
        p, q = self.__get_prime_with_no_dominant_divider(n), self.__get_prime_with_no_dominant_divider(n)
        while p == q:
            q = self.__get_prime_with_no_dominant_divider(n)

        d = 0
        while math.gcd(d, (p - 1)*(q - 1)) != 1:
            d = randint(0, int(Decimal(1/3) * Decimal(p*q)**Decimal(1/4)))
        e = pow(d, -1, (p - 1)*(q - 1))

        return (d, e, p*q)

    def get_weak_p1_pollard_key(self, n):
        p = self.__get_b_smooth_prime(n, 2**10)
        q = get_random_prime(n)

        d = 0
        while math.gcd(d, (p - 1)*(q - 1)) != 1:
            d = randint(0, int(Decimal(1/3) * Decimal(p*q)**Decimal(1/4)))
        e = pow(d, -1, (p - 1)*(q - 1))

        return (d, e, p*q)

    def get_weak_rho_pollard_key(self, n):
        p, q = get_random_prime(n), get_random_prime(n)
        e = 0
        while math.gcd(e, (p - 1)*(q - 1)) != 1:
            e = randint(0, (p - 1)*(q - 1))
        d = pow(e, -1, (p - 1)*(q - 1))

        return (d, e, p*q)

    def __get_prime_with_no_dominant_divider(self, n):
        divider_num = 4
        max_divider_len = n // divider_num 
        primes_p = [get_random_prime(max_divider_len) for _ in range(divider_num)]

        i = 0
        while not is_prime(math.prod(primes_p) + 1):
            degr = [randint(1, 5) for _ in range(divider_num)]
            primes_p = [get_random_prime(max_divider_len // degr[i])**degr[i] for i in range(divider_num)]
            i += 1
            if i % 100 == 0 and max_divider_len > 4:
                divider_num += 1
                max_divider_len = n // divider_num

        return math.prod(primes_p) + 1

    def __get_b_smooth_prime(self, n, B):
        p1 = 2

        while not is_prime(p1 + 1) or p1 == 2:
            p1 = 1
            while p1.bit_length() < n:
                deg = randint(1, 5)
                devider = randint(1, B)**deg
                p1 *= devider

        return p1 + 1