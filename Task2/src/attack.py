import logging
import signal

class Attack(object):

    def __init__(self, timeout=60):
        self._logger = logging.getLogger("RSA attack logger")
        self._timeout = timeout
        #signal.signal(signal.SIGALRM, self.__timeout_handler)
        self._attack_func = None

    def attack(self, keys, cipher=None):
        #signal.setitimer(signal.ITIMER_REAL, self._timeout, 0)
        res = self._attack_func(keys, cipher)
        
        return res
        
    def __timeout_handler(self):
        raise TimeoutError("Timeout exception")