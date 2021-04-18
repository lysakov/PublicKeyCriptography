from keygen import KeyGen
from rho_pollard import RhoPollardAttack
from wiener import WienerAttack
from low_exponent import LowExponentAttack
from cycle import CycleAttack
from p1_pollard import P1Pollard

from random import choice
import logging

if __name__ == "__main__":
    print("1. Weak keys generator.")
    print("2. Key attack.")

    n = ""
    while n != "1" and n != "2":
        n = input()

    if n == "1":
        print("Enter sequence of numbers, splitted by comma.")
        print("1. Rho-Pollard attack.")
        print("2. p-1 Pollard attack.")
        print("3. Low exponent attack.")
        print("4. Wiener attack.")
        print("5. Cycle attack.")

        n = ""
        n = input()
        i = int(choice(n.split(',')))

        print("Enter security parametr:")
        n = input()

        keygen = KeyGen()
        d, e, N = None, None, None
        if i == 1:
            d, e, N = keygen.get_weak_rho_pollard_key(int(n))
        elif i == 2:
            d, e, N = keygen.get_weak_p1_pollard_key(int(n))
        elif i == 3:
            d, e, N = keygen.get_weak_low_exponent_key(int(n))
        elif i == 4:
            d, e, N = keygen.get_weak_wiener_keys(int(n))
        elif i == 5:
            d, e, N = keygen.get_weak_cycle_key(int(n))

        print(f"d = {d}")
        print(f"e = {e}")
        print(f"N = {N}")

    elif n == "2":
        logging.basicConfig(filename="log.txt", level=logging.INFO, filemode="w")
        print("Enter time limit:")
        n = int(input())
        print("Enter open exponent:")
        e = int(input())
        print("Enter N:")
        N = int(input())
        print("Enter encrypted message:")
        c = int(input())

        attacks = [RhoPollardAttack(n), P1Pollard(timeout=n), LowExponentAttack(n), WienerAttack(n), CycleAttack(n)]
        for attack in attacks:
            try:
                attack.attack((e, N), c)
            except TimeoutError:
                attack.log("Time limit reached")