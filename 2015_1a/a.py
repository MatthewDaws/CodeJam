# -*- coding: utf-8 -*-
num_cases = int(input())

for case in range(1, num_cases+1):
    num_readings = int(input())
    readings = [int(x) for x in input().split()]
    diffs = [x-y for x, y in zip(readings[:-1], readings[1:])]
    poss = [x for x in diffs if x > 0]
    if len(poss) == 0:
        one = 0
        rate = 0
        two = 0
    else:
        one = sum( poss )
        rate = max( poss )
        two = sum( min(x,rate) for x in readings[:-1] )
    output = "{} {}".format(one, two)
    print("Case #{}: {}".format(case, output))