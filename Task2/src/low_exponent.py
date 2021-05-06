from attack import Attack
from decimal import Decimal

import decimal

class LowExponentAttack(Attack):

    def __init__(self, timeout=60):
        super().__init__(timeout=timeout)
        self._attack_func = self.__low_exponent

    def __low_exponent(self, keys, cipher=None):
        e, N = keys
        c = cipher
        self._logger.info("***LOW EXPONENT ATTACK***")
        if c is None:
            raise ValueError("Impossible to apply low exponent attack without ciphered message.")

        self._logger.info(f"Searching for m: m**{e} = {c} + k*{N} for k = 0, 1, 2, ...")
        k = 0
        m = self.__n_root(c, e)
        stop_flag = c + k*N == m**e
        self._logger.info(f"k = {0}: {c} == {m}**{e} => {stop_flag}")

        while not stop_flag:
            k += 1
            m = self.__n_root(c + k*N, e)
            stop_flag = c + k*N == m**e
            self._logger.info(f"k = {k}: {c} + {k}*{N} == {m}**{e} => {stop_flag}")
            if k % 10000 == 0:
                self._logger.info(f"{k} iteration were made. Public exponent may be not so small.")

        return m

    
    def __n_root(self, x, n):
        return int((Decimal(x)**(Decimal(1)/Decimal(n))).quantize(Decimal(1.), rounding=decimal.ROUND_HALF_UP))