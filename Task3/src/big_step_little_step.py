from attack import Attack

class GelfondAttack(Attack):

    def __init__(self, t=2, timeout=60):
        self._t = t
        super().__init__(timeout=timeout)
        self._attack_func = self.__gelfond_attack

    def __gelfond_attack(self, keys, cipher):
        self._logger.info("Gelfond attack:")
        y, g, p = keys
        self._logger.info(f"{g}^x = {y} mod {p}")
        a = pow(g, self._t, p)

        self._logger.info("Building dictationary...")
        dictionary = {}

        for i in range(p // self._t + 1):
            dictionary[pow(a, i, p)] = i
        self._logger.info(f"Dictationary with {p // self._t + 1} records was build")

        el, r = y, 0
        while r < self._t:
            if el in dictionary:
                x = (dictionary[el]*self._t - r) % (p - 1)
                self._logger.info(f"x = {x}")
                return x
            else:
                el *= g
                el %= p
                r += 1

        return None