from attack import Attack
from math import gcd
from utils import *

class RhoPollardAttack(Attack):

    def __init__(self, timeout=60, a=2, b=2, f=lambda x: x**2 + 1):
        super().__init__(timeout)
        self._a = a
        self._b = b
        self._f = f
        self._attack_func = self.__rho_pollard

    def __rho_pollard(self, keys, cipher=None):
        e, N = keys
        d = 1

        self._logger.info("***rho-POLLARD ATTACK***")
        self._logger.info(f"a0 = {self._a}, b0 = {self._b}, f = x**2 + 1")
        i = 1
        while d == 1:
            self._a = self._f(self._a) % N
            self._b = self._f(self._f(self._b)) % N
            d = gcd(self._a - self._b, N)
            self._logger.info(f"a{i} = {self._a}, b{i} = {self._b}, d{i} = {d}")
            i += 1

        return d if d != N else None