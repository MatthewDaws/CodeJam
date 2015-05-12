import math

def product_old(vector):
    x = 1
    for y in vector:
        x *= y
    return x

def product(vector):
    if 0.0 in vector:
        return 0
    v = [math.log(x) for x in vector]
    v.sort()
    return math.exp( sum(v) )

def solve(A, B, prob):
    prob_okay = product(prob)
    prob_not = 0
    for length in range(len(prob)):
        prob_not += product( prob[:length] ) * (1.0 - prob[length])
    presses_okay = B - A + 1
    presses_not = presses_okay + B + 1
    options = []
    for length in range(len(prob)-1, -1, -1):
        options.append( presses_okay * prob_okay + presses_not * prob_not )
        presses_okay += 2
        presses_not += 2
        prob_swap = product( prob[:length] ) * (1.0 - prob[length])
        prob_okay += prob_swap
        prob_not -= prob_swap
    options.append( presses_okay * prob_okay + presses_not * prob_not )
    # Give up case
    options.append( B + 2 )
    return min(options)

num_cases = int(input())
for case in range(1, num_cases+1):
    A, B = [int(x) for x in input().split()]
    p = [float(x) for x in input().split()]
    print("Case #{}: {:.6f}".format(case, solve(A,B,p)))
    