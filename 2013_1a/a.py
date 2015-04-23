# -*- coding: utf-8 -*-
import math

def intsqrt(x):
    y = math.floor(math.sqrt(x))
    y = ( y + x//y ) // 2
    y = ( y + x//y ) // 2
    y = ( y + x//y ) // 2
    return y

num_cases = int(input())

for case in range(1, num_cases+1):
    r, t = [int(x) for x in input().split()]
    b, c = r+r-1, -t
    #N = (-b + math.sqrt(b*b - 4*a*c)) / (a+a)
    disc = b*b - 8*c
    #N = -b + math.sqrt(disc)
    N = intsqrt(disc) - b
    output = math.floor(N) // 4
    print("Case #{}: {}".format(case, output))