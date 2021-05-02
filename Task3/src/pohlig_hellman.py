from attack import Attack
from utils import *

class PohligHellmanAttack(Attack):

    def __init__(self, timeout=60):
        super().__init__(timeout=timeout)
        self._attack_func = self.__pohlig_hellman

    def __pohlig_hellman(self, keys, cipher):
        self._logger.info("Pohlig-Hellman attack:")
        y, g, p = keys
        self._logger.info(f"{g}^x = {y} mod {p}")
        self._logger.info("Factorizing p - 1...")
        factorization = factorize(p - 1)
        self._logger.info(f"p - 1 factorization: {factorization}")
        x = []

        for q, a in factorization.items():
            table = self.__create_table(g, p, q)
            x_q = []
            inv_g = pow(g, -1, p)
            for i in range(a):
                exp = sum([x_q[j] * q**j for j in range(i)])
                el = y * pow(inv_g, exp, p)
                x_q.append(table[pow(el, (p - 1) // q**(i + 1), p)])
            x.append((sum([x_q[i] * q**i for i in range(a)]), q**a))
            self._logger.info(f"x = {x[-1][0]} mod {q}**{a}")

        res = self.__cmt(x, p - 1)
        self._logger.info(f"x = {res}")

        return res


    def __create_table(self, g, p, q):
        self._logger.info(f"Building table for q = {q}...")
        table = {}
        for i in range(q):
            table[pow(g, i*(p - 1)//q, p)] = i
        self._logger.info("Table was build.")

        return table

    def __cmt(self, remainders, m):
        res = 0
        for r, n in remainders:
            tmp = m // n
            res += r * tmp * pow(tmp, -1, n)

        return res % m