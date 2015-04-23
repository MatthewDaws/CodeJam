# -*- coding: utf-8 -*-
import math
import itertools

num_cases = int(input())

for case in range(1, num_cases+1):
    E, R, N = [int(x) for x in input().split()]
    v = [int(x) for x in input().split()]

    if R >= E:
        # Optimal is just spend E on everything
        output = E * sum(v)
    elif N == 1:
        output = E * v[0]
    elif N == 2:
        output = max( E * v[0] + R * v[1], R * v[0] + E * v[1] )
    else:
        choices = list(range(E+1))
        best = R * sum(v[:-1]) + E * v[-1]
        for e0 in range(R, E+1):
            for ee in itertools.product(choices, repeat = N-2):
                energy = E - e0 + R
                gain = e0 * v[0]
                for ei, vi in zip(ee, v[1:]):
                    if ei > energy:
                        gain = -1
                        break
                    gain += ei * vi
                    energy = min(E, energy + R - ei)
                # Last case
                gain += energy * v[-1]
                if gain > best:
                    best = gain
        output = best        

    print("Case #{}: {}".format(case, output))
