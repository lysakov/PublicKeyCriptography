import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from keygen import KeyGen
from rho_pollard import RhoPollardAttack
from wiener import WienerAttack
from low_exponent import LowExponentAttack
from cycle import CycleAttack
from p1_pollard import P1Pollard
from utils import *

import logging
from math import gcd

class Test(unittest.TestCase):

    def setUp(self):
        self.keygen = KeyGen()
        logging.basicConfig(filename="log.txt", level=logging.INFO, filemode="w", format="%(message)s")

    def test_miller_rabin(self):
        p = 223
        self.assertEqual(True, miller_rabin_test(p))

    def test_rho_pollard(self):
        d, e, N = self.keygen.get_weak_rho_pollard_key(32)
        rho_pollard = RhoPollardAttack()
        p = rho_pollard.attack((e, N))
        self.assertEqual(N % p, 0)

    def test_wiener(self):
        d, e, N = self.keygen.get_weak_wiener_keys(128)
        wiener = WienerAttack()
        keys = wiener.attack((e, N))
        self.assertEqual(keys[0]*keys[1], N)

    def test_low_exponent(self):
        d, e, N = self.keygen.get_weak_low_exponent_key(64)
        low_exponent = LowExponentAttack()
        m = 2 #randint(0, N)
        m1 = low_exponent.attack((e, N), pow(m, e, N))
        self.assertEqual(m1, m)

    def test_cycle(self):
        d, e, N = self.keygen.get_weak_cycle_key(32)
        m = randint(0, N)
        cycle = CycleAttack()
        p = cycle.attack((e, N), pow(m, e, N))
        self.assertEqual(N % p, 0)

    def test_p1_pollard(self):
        d, e, N = self.keygen.get_weak_p1_pollard_key(100)
        p1_pollard = P1Pollard(timeout=1)
        p = p1_pollard.attack((e, N))
        self.assertEqual(N % p, 0)


if __name__ == "__main__":
    unittest.main()