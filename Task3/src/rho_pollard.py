from attack import Attack
from math import log2, floor, gcd

class RhoPollardAttack(Attack):

    def __init__(self, timeout=60):
        super().__init__(timeout=timeout)
        self._attack_func = self.__rho_pollard

    def __rho_pollard(self, keys, cipher):
        self._logger.info("Rho-Pollard attack")
        y, g, p = keys
        self._logger.info(f"{g}^x = {y} mod {p}")
        h = (y, 0, 1)
        T = {0 : h}
        
        for i in range(1, p):
            h = self.__f(y, g, p, h)
            self._logger.info(f"i = {i}, h = {h[0]}. Showing table content:")
            for ind, el in T.items():
                self._logger.info(f"{ind}: h = {el[0]} deg(g) = {el[1]} deg(y) = {el[2]}")
                if el[0] == h[0]:
                    self._logger.info(f"Cycle found")
                    dx = h[1] - el[1]
                    dy = el[2] - h[2]
                    x, d = self.__solve_linear(dy, dx, p - 1)
                    for i in range(d):
                        if pow(g, x + i*(p - 1)//d, p) == y:
                            x = (x + i*(p - 1)//d) % (p - 1)
                            self._logger.info(f"x = {x}")
                            return x

            T[self.__v2(i)] = h

        return None

    def __v2(self, s):
        i = 0
        while s % 2**i == 0:
            i += 1

        return i - 1

    def create_set(self, s):
        s_set = []
        for i in range(floor(log2(s)) + 1):
            q = s // 2**i
            q = q - 1 if q % 2 == 0 else q
            s_set.append(q * 2**i - 1)

        return s_set

    def modify_set(self, s, s_set):
        i = 0
        while (s + 1) % 2**i == 0:
            i += 1
        i -= 1

        if len(s_set) <= i:
            s_set.append(s)
        else:
            s_set[i] = s

    def __f(self, y, g, p, h):
        if h[0] % 3 == 1:
            return (y*h[0] % p, h[1], (h[2] + 1) % (p - 1))
        elif h[0] % 3 == 0:
            return (pow(h[0], 2, p), 2*h[1] % (p - 1), 2*h[2] % (p - 1))
        else:
            return (g*h[0] % p, (h[1] + 1) % (p - 1), h[2])

    def __solve_linear(self, a, b, p):
        d = gcd(a, p)
        if d == 1:
            return b*pow(a, -1, p) % p, 1

        p //= d
        a %= p
        b %= p
        
        return b*pow(a, -1, p) % p, d