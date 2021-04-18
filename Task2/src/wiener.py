from attack import Attack
from utils import get_continued_fraction
from math import isqrt

class WienerAttack(Attack):

    def __init__(self, timeout=60):
        super().__init__(timeout=timeout)
        self._attack_func= self.__wiener

    def __wiener(self, keys, cipher=None):
        e, N = keys
        cont_fraction = get_continued_fraction(e, N)
        self._logger.info("\n***WIENER ATTACK***")
        self._logger.info(f"\ne/N = {e}/{N} = {cont_fraction}")

        k = [0, 1]
        d = [1, 0]
        for i in range(len(cont_fraction)):
            k.append(cont_fraction[i] * k[i + 1] + k[i])
            d.append(cont_fraction[i] * d[i + 1] + d[i])

        for i in range(2, len(k)):
            if k[i] == 0:
                continue
            phi, r = divmod(e*d[i] - 1, k[i])
            if r == 0:
                self._logger.info(f"\nSolving equation: x**2 + {-(N - phi + 1)}*x + {N} = 0")
                p, q = self.__solve_eqv(N, phi)
                if p is None:
                    self._logger.info("\nEquation has no integer roots. Contunue searching k and d...")
                    continue
                self._logger.info(f"\np = {p}, q = {q}")
                if p*q == N:
                    return p, q
                else:
                    self._logger.info(f"{p} * {q} != {N}")
                    continue

        self._logger.info("\nUnable to find factorization of N")

        return None

    def __solve_eqv(self, N, phi):
        p = -(N - phi + 1)
        q = N
        D = self.__sqrt(p**2 - 4*q)
        if D is None:
            return None, None

        x1 = (-p + D) // 2
        x2 = (-p - D) // 2

        return x1, x2

    def __sqrt(self, x):
        sqrt = isqrt(x)
        if sqrt**2 == x:
            return sqrt
        
        return None