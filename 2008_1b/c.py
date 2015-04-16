# -*- coding: utf-8 -*-
def solve(K, posin):
    """K = number of cards
    posin = array of indices (1 through K) we care about"""
    positions = posin[:]
    output = [0] * len(positions)
    lefttofind = len(positions)
    card = 1
    position = 0   # position is zero offset
    remaining = K
    while lefttofind > 0:
        position += card - 1
        position %= remaining
        # "Delete" this position
        for i in range(len(positions)):
            if positions[i] == position + 1:
                output[i] = card
                positions[i] = 0
                lefttofind -= 1
            if positions[i] > position + 1:
                positions[i] -= 1
        # Next loop
        card += 1
        remaining -= 1
    return output

num_cases = int(input())
for case in range(1, num_cases+1):
    K = int(input())
    slots = [int(x) for x in input().split()]
    slots = slots[1:]
    print("Case #{}: {}".format(case, " ".join(str(x) for x in solve(K,slots))))
