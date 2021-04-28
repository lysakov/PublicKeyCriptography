from attack import Attack
from utils import *

class PohligHellmanAttack(Attack):

    def __init__(self, timeout=60):
        super().__init__(timeout=timeout)
        self._attack_func = self.__pohlig_hellman

    def __pohlig_hellman(self, keys, cipher):
        y, g, p = keys
        factorization = factorize(p - 1)
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

        return self.__cmt(x, p - 1)


    def __create_table(self, g, p, q):
        table = {}
        for i in range(q):
            table[pow(g, i*(p - 1)//q, p)] = i

        return table

    def __cmt(self, remainders, m):
        res = 0
        for r, n in remainders:
            tmp = m // n
            res += r * tmp * pow(tmp, -1, n)

        return res % m