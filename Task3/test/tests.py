import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from utils import *
from keygen import KeyGenerator
from gelfond import GelfondAttack
from pohlig_hellman import PohligHellmanAttack
from rho_pollard import RhoPollardAttack

import logging

class Test(unittest.TestCase):

    def setUp(self):
        self.keygen = KeyGenerator()
        logging.basicConfig(filename="log.txt", 
                            level=logging.INFO, 
                            filemode="w",
                            format="%(message)s")

    def test_factorize(self):
        p = get_random_prime(32)
        factorization = factorize(p - 1)
        q = 1
        for factor in factorization.items():
            q *= factor[0]**factor[1]

        self.assertEqual(q + 1, p)

    def test_gelfond(self):
        gelfond = GelfondAttack(2)
        y, g, p = self.keygen.get_key(16)
        x = gelfond.attack((y, g, p))
        self.assertEqual(pow(g, x, p), y)

    def test_pohlig_hellman(self):
        pohlig_hellman = PohligHellmanAttack()
        y, g, p = self.keygen.get_vulnerable_pohlig_hellman_key(128)
        x = pohlig_hellman.attack((y, g, p))
        self.assertEqual(pow(g, x, p), y)

    def test_rho_pollard(self):
        rho_pollard = RhoPollardAttack()
        y, g, p = self.keygen.get_key(16)
        x = rho_pollard.attack((y, g, p))
        self.assertEqual(pow(g, x, p), y)        

if __name__ == "__main__":
    unittest.main()