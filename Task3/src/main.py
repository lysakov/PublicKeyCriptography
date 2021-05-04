from keygen import KeyGenerator
from rho_pollard import RhoPollardAttack
from gelfond import GelfondAttack
from pohlig_hellman import PohligHellmanAttack

from random import choice
import logging

if __name__ == "__main__":
    print("1. Key analyzer.")
    print("2. Weak Pohlig-Hellman key generator.")

    n = ""
    while n != "1" and n != "2":
        n = input()

    if n == "2":
        print("Enter key length:")
        n = int(input())
        keygen = KeyGenerator()
        y, g, p = keygen.get_vulnerable_pohlig_hellman_key(n)
        print("y =", y)
        print("g =", g)
        print("p =", p)


    elif n == "1":
        logging.basicConfig(filename="log.txt", level=logging.INFO, filemode="w")
        print("Enter time limit:")
        n = int(input())
        print("Enter open exponent:")
        e = int(input())
        print("Enter N:")
        N = int(input())
        print("Enter encrypted message:")
        c = int(input())

        attacks = [RhoPollardAttack(n), PohligHellmanAttack(n), GelfondAttack(timeout=n)]
        for attack in attacks:
            try:
                attack.attack((e, N), c)
            except TimeoutError:
                attack.log("Time limit reached")