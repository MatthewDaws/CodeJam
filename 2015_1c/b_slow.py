import functools, itertools

from collections import Counter
from fractions import Fraction


def solve(letters, target, S):
    ld = Counter(letters)
    for c in target:
        if c not in ld:
            return 0
    global letterdict
    letterdict = { c : Fraction(ld[c],len(letters)) for c in ld }
    L = len(target)
    maximum = 0
    expect = 0
    for choice in itertools.product(letters, repeat = S):
        x = "".join(choice)
        count = sum( x[i:i+L] == target for i in range(S - L + 1) )
        maximum = max(maximum, count)
        expect += count
    expect /= len(letters)**S
    return maximum - expect

num_cases = int(input())
for case in range(1, num_cases+1):
    K, L, S = [int(x) for x in input().split()]
    typewriter = input()
    target = input()
    print("Case #{}: {:.6f}".format(case, solve(typewriter, target, S)))