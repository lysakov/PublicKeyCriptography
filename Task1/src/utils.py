import sys

from Cryptodome.Hash import SHA256
from Cryptodome.Util import number

from math import prod

def int_to_bytes(n : int) -> bytes:
    return n.to_bytes((n.bit_length() + 7) // 8, "little")

def bytes_to_int(bytes_arr : bytes) -> int:
    return int.from_bytes(bytes_arr, "little")

def string_to_bytes(string : str) -> bytes:
    return string.encode("utf-16")

def bytes_to_string(bytes_arr : bytes) -> str:
    return bytes_arr.decode("utf-16")

def compute_hash(data : bytes) -> bytes:
    return SHA256.new(data).digest()

def byte_length(x : int) -> int:
    return (x.bit_length() + 7) // 8 

def sqrt_mod(a : int, p : int) -> int:
    m = 0
    s = p - 1
    while s % 2 != 1:
        m += 1
        s //= 2

    j, tmp_a = None, None
    tmp_b = pow(generate_non_quadratic_residue(p), s, p)

    if m == 1:
        j = 0
    else:
        tmp_a = pow(a, s, p)
        A = [pow(tmp_a, pow(2, i, p - 1), p) for i in range(m - 1)]
        B = [pow(tmp_b, pow(2, i, p - 1), p) for i in range(m - 1)]
        eps = 1 if A[::-1][0]%p == p - 1 else 0
        j = eps

        for t in range(1, m - 1):
            get_bit = lambda x, i: (x >> i) & 1 
            eps = A[::-1][t] * prod([B[::-1][t - i]**get_bit(j, i - 1) for i in range(1, t + 1)])
            eps = 1 if eps%p == p - 1 else 0
            j += pow(2, t) * eps

    return pow(tmp_b, j, p) * pow(a, (s + 1) // 2, p) % p

def generate_non_quadratic_residue(p : int) -> int:
    a = number.getRandomRange(0, p - 1)

    while pow(a, (p - 1)//2, p) == 1:
        a = number.getRandomRange(0, p - 1)

    return a

def generate_quadratic_residue(p : int) -> int:
    a = number.getRandomRange(0, p - 1)

    while pow(a, (p - 1)//2, p) == p - 1:
        a = number.getRandomRange(0, p - 1)

    return a