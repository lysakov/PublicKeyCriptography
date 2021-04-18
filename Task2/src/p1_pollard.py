from utils import *
from attack import Attack
from random import randint
from math import gcd

class P1Pollard(Attack):

    def __init__(self, B=2**7, timeout=60):
        super().__init__(timeout=timeout)
        self._B = B
        self._attack_func = self.__p1_pollard

    def __p1_pollard(self, keys, cipher=None):
        self._logger.info(f"\n***p - 1 POLLARD ATTACK***")
        e, N = keys

        while True:
            self._logger.info(f"\nB = {self._B}")
            a = randint(2, N - 1)
            self._logger.info(f"\na = {a}")
            d = gcd(a, N)
            if d > 2:
                return d

            for q in range(self._B):
                if is_prime(q):
                    l = self.__log(q, N)
                    a = pow(a, pow(q, l), N)
                    self._logger.info(f"\nq = {q}, l = {l}, a = {a}")

            d = gcd(a - 1, N)
            if d != 1 and d != N:
                self._logger.info(f"\np = {d}, q = {N // d}")
                return d
            else:
                self._B = self._B*2

    def __log(self, p, N):
        res = 1
        while p**res < N:
            res += 1

        return res - 1