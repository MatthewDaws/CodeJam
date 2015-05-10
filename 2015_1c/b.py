import functools

from collections import Counter
from fractions import Fraction

def prob_exact(target, copies, length, postfix):
    """As below, but == `copies`"""
    return prob(target, copies, length, postfix) - prob(target, copies + 1, length, postfix)

@functools.lru_cache(maxsize = None)
def prob(target, copies, length, postfix):
    """Returns probability a string of `length` contains >= `copies` of `target` and ends in `postfix`"""
    if len(postfix) == 0:
        if copies <= 0: return 1
        if length < len(target): return 0
        if length == len(target):
            if copies > 1: return 0
            p = 1
            for c in target:
                p *= letterdict[c]
            return p
        return ( prob(target, copies, length - 1, "") +
            prob_exact(target, copies - 1, length - 1, target[:-1]) * letterdict[target[-1]] )
    # So have a postfix.
    if length < len(postfix): return 0
    if length == len(postfix):
        if copies > 0: return 0 # len(postfix) < len(target)
        p = 1
        for c in postfix:
            p *= letterdict[c]
        return p
    # Does postfix overlap exactly with end of target?
    if target[-len(postfix):] == postfix:
        return ( prob(target, copies, length - 1, postfix[:-1]) * letterdict[postfix[-1]] +
            prob_exact(target, copies - 1, length - 1, target[:-1]) * letterdict[postfix[-1]] )
    return prob(target, copies, length - 1, postfix[:-1]) * letterdict[postfix[-1]]

def solve(letters, target, S):
    prob.cache_clear()
    ld = Counter(letters)
    for c in target:
        if c not in ld:
            return 0
    global letterdict
    letterdict = { c : Fraction(ld[c],len(letters)) for c in ld }
    # In business
    copies = 1
    expect = 0
    while True:
        p = prob(target, copies, S, "")
        if p == 0:
            break
        expect += p
        copies += 1
    maximum = copies - 1
    return float(maximum - expect)

num_cases = int(input())
for case in range(1, num_cases+1):
    K, L, S = [int(x) for x in input().split()]
    typewriter = input()
    target = input()
    print("Case #{}: {:.6f}".format(case, solve(typewriter, target, S)))