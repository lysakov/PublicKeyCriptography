from attack import Attack

class GelfondAttack(Attack):

    def __init__(self, t=2, timeout=60):
        self._t = t
        super().__init__(timeout=timeout)
        self._attack_func = self.__gelfond_attack

    def __gelfond_attack(self, keys, cipher):
        y, g, p = keys
        a = pow(g, self._t, p)

        self._logger.info("\nBuilding dictationary...")
        dictionary = {}

        for i in range(p // self._t + 1):
            dictionary[pow(a, i, p)] = i

        el, r = y, 0
        while r < self._t:
            #print(r)
            if el in dictionary:
                return (dictionary[el]*self._t - r) % (p - 1)
            else:
                el *= g
                el %= p
                r += 1

        return None