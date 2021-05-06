from attack import Attack
from utils import *
from math import gcd

class CycleAttack(Attack):

    def __init__(self, timeout=60):
        super().__init__(timeout=timeout)
        self._attack_func = self.__cycle

    def __cycle(self, keys, cipher=None):
        self._logger.info("***CYCLE ATTACK***")
        e, N = keys
        c = cipher
        if c is None:
            raise ValueError("Impossible to apply low cycle attack without ciphered message.")

        c1 = pow(c, e, N)
        d = gcd(c1 - c, N)
        cnt = 1
        while d == 1 or d == N:
            c1 = pow(c1, e, N)
            d = gcd(c1 - c, N)
            cnt += 1

        self._logger.info(f"N was factorized in {cnt} iterations")

        return d