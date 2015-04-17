import numpy as np
import math

def calc_probs(N, k):
    """Returns prob a[j] == k for varying j"""
    prob = np.zeros(N, dtype=np.float64)
    prob[k] = 1.0
    for i in range(N):
        val = prob[i] / N
        prob = prob*(1-1/N) + val
        prob[i] = 1/N
    return prob

# probs[k][j] = prob(a[j] == k | BAD)
probs = [calc_probs(1000,k) for k in range(1000)]

def nb_classifier(a):
    global probs
    prob = 0.0
    for j in range(len(a)):
        prob += math.log( probs[a[j]][j] )
    probgood = -math.log(N) * N
    #print(prob, probgood)
    if prob >= probgood:
        return "BAD"
    return "GOOD"

T = int(input())
for case in range(1, T+1):
    N = int(input())
    if N != 1000:
        raise Exception("N should be 1000")
    a = [int(x) for x in input().split()]
    output = nb_classifier(a)
    print("Case #{}: {}".format(case, output))
