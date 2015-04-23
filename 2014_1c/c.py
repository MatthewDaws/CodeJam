# -*- coding: utf-8 -*-
import math

def binary_search(func):
    """Find the maximum integer k>=1 with func(k) == True.
    Assumed that func(1) == True !"""
    high = 2
    while func(high):
        high += high
    low = high // 2
    while high - low > 1:
        mid = (low+high) // 2
        if func(mid):
            low = mid
        else:
            high = mid
    return low

def test1(n, m, K):
    # Hurrah for closures
    def func(k):
        return k+k <= n+1 and k+k <= m+1 and 4*k*(k-1) <= 2*(n*m-K)
    return func

def test2(n, m, K):
    # Hurrah for closures
    def func(k):
        return k+k+1 <= n+1 and k+k+1 <= m+1 and 3*k*(k-1) + k*(k+1) <= 2*(n*m-K)
    return func

def test3(n, m, K):
    # Hurrah for closures
    def func(k):
        return k+k <= n and k+k <= m and k*(k-1) + k*(k+1) <= n*m-K
    return func

def test4(n, m, K):
    # Hurrah for closures
    def func(k):
        return k+k+1 <= n and k+k+1 <= m and 3*k*(k+1) + k*(k-1) <= 2*(n*m-K)
    return func

def find_best(n, m, K):
    """Find the best arrangement to enclose at least `K` in an `n` by `m` grid.
    Assumes that n*m >= K"""
    # Special cases
    if n < m:
        n, m = m, n
    # So now n >= m
    if m == 1:
        # Best we can do is K
        return K
    # Can probably optimise as know k4 <= k3 <= k2 <= k1
    cases = []
    if test1(n,m,K)(1):
        k = binary_search(test1(n,m,K))
        cases.append(4*k)
    if test2(n,m,K)(1):
        k = binary_search(test2(n,m,K))
        cases.append(4*k+1)
    if test3(n,m,K)(1):
        k = binary_search(test3(n,m,K))
        cases.append(4*k+2)
    if test4(n,m,K)(1):
        k = binary_search(test4(n,m,K))
        cases.append(4*k+3)
    return n+n+m+m - max(cases)

#for n in range(1, 6):
#    for m in range(1, 6):
#        if n*m>=8:
#            print(n,m, find_best(n, m, 8))
#exit()

num_cases = int(input())
for case in range(1, num_cases+1):
    N, M, K = [int(x) for x in input().split()]

    output = min( find_best(n,m,K) for n in range(1,N+1) for m in range(1,M+1)
                    if n*m >= K )

    print("Case #{}: {}".format(case, output))
