# -*- coding: utf-8 -*-

def gcd(a, b):
    while b > 0:
        a, b = b, a % b
    return a

num_cases = int(input())
for case in range(1, num_cases+1):
    P, Q = [int(x) for x in input().split("/")]

    g = gcd(P, Q)
    P //= g
    Q //= g
    if P > Q:
        raise Exception("Fraction not <=1")

    # Find greatest power of 2 dividing Q
    M = 0
    while Q % 2 == 0:
        M += 1
        Q //= 2
    if Q != 1 or M > 40:
        output = "impossible"
    else:
        P *= 2**(40-M)
        # Find max n with P>=2**n
        n = max( k for k in range(41) if P >= 2**k )
        output = 40 - n

    print("Case #{}: {}".format(case, output))