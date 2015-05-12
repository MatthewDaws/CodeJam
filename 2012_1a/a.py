import math

def solve(A, B, prob):
    prob_okay = 1.0
    prob_not = 0.0
    prod = 1.0
    presses_okay = A + B + 1
    presses_not = presses_okay + B + 1
    options = []
    for p in prob:
        options.append( presses_okay * prob_okay + presses_not * prob_not )
        presses_okay -= 2
        presses_not -= 2
        prob_not += prod * (1 - p)
        prob_okay -= prod * (1 - p)
        prod *= p
    options.append( presses_okay * prob_okay + presses_not * prob_not )
    # Give up case
    options.append( B + 2 )
    return min(options)

num_cases = int(input())
for case in range(1, num_cases+1):
    A, B = [int(x) for x in input().split()]
    p = [float(x) for x in input().split()]
    print("Case #{}: {:.6f}".format(case, solve(A,B,p)))
    