from random import randint

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

def get_continued_fraction(a : int, b : int) :
    frac = []
    x, y = a, b

    while x % y != 0:
        frac.append(x//y)
        x, y = y, x%y

    frac.append(x//y)

    return frac