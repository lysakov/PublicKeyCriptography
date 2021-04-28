from random import randint
from math import isqrt

def miller_rabin_test(n, k=10):
    if n == 2 or n == 3:
        return True

    if n % 2 == 0 or n == 1:
        return False

    s = 0
    t = n - 1
    while t % 2 == 0:
        s += 1
        t //= 2

    for _ in range(k):
        a = randint(2, n - 2)
        x = pow(a, t, n)
        if x == 1 or x == n - 1:
            continue

        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
            elif x == 1:
                return False
        
        if x == n - 1:
            continue
        else:
            return False

    return True

def get_random_prime(n : int) -> int:
    p = randint(2**n, 2**(n + 1) - 1)

    while not miller_rabin_test(p):
        p = randint(2**n, 2**(n + 1) - 1)

    return p

def is_prime(n : int) -> bool:
    return miller_rabin_test(n)

def factorize(x : int) -> dict:
    if is_prime(x):
        return {x : 1}

    def div(x, p, factorization):
        s = 0
        while x % p == 0:
            x //= p
            s += 1
        if s != 0:
            factorization[p] = s

        return x

    factorization = {}
    x = div(x, 2, factorization)
    for i in range(3, isqrt(x) + 1, 2):
        if is_prime(i):
            x = div(x, i, factorization)
            if x == 1:
                break
            if is_prime(x):
                factorization[x] = 1
                break

    return factorization

def get_primitive_root(p : int) -> int:
    factorization = factorize(p - 1)
    g = randint(2, p - 1)

    def is_primetive_root(g, p, factorization):       
        for q in factorization.keys():
            if pow(g, (p - 1)//q, p) == 1:
                return False

        return True

    while not is_primetive_root(g, p, factorization):
        g = randint(2, p - 1)

    return g