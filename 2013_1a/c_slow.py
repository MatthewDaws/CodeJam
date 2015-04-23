# -*- coding: utf-8 -*-
import math
import itertools

num_cases = int(input())

for case in range(1, num_cases+1):
    R, N, M, K = [int(x) for x in input().split()]

    # For small 1, N=3, M=5 so A ranges from [2,2,2] to [5,5,5]
    # So possible products are from 1 to 5**3 = 125

    output = []
    for r in range(R):
        prods = [int(x) for x in input().split()]
        choices = list(range(2, M+1))
        prob = dict()
        for A in itertools.product(choices, repeat = N):
            possible_products = []
            for subsetbin in range(2**N):
                subset = [ A[i] for i in range(N) if ( subsetbin & (2**i) ) > 0 ]
                prod = 1
                for x in subset:
                    prod *= x
                possible_products.append(prod)
            # Probability
            prob[A] = 1
            for pi in prods:
                prob[A] *= sum( p==pi for p in possible_products )
        bestA = []
        bestprob = 0
        for A in prob:
            if prob[A] >= bestprob:
                bestA = A
                bestprob = prob[A]
        output.append("".join(str(x) for x in bestA))

    print("Case #{}:".format(case))
    for s in output:
        print(s)

