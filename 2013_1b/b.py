# -*- coding: utf-8 -*-

def find_layer(N):
    # Solve n(2n-1) < N <= (n+1)(2n+1)
    low = 0
    high = 1
    while high * (high + high - 1) < N:
        high += high
    while high - low > 1:
        mid = (high + low) // 2
        if mid * (mid + mid -1 ) < N:
            low = mid
        else:
            high = mid
    return low

import math
def choices(N, k):
    return math.factorial(N) / (math.factorial(k) * math.factorial(N-k))

def merge(choices):
    output = dict()
    for p in choices:
        pair = (p[0],p[1])
        prob = p[2]
        if pair not in output:
            output[pair] = 0.0
        output[pair] += prob
    return [ (p[0], p[1], output[p]) for p in output ]

def calc_prob(layer, Y, delta):
    # layer = 1 then interested in
    # [0,0] -> [1,0] or [0,1] with 50% prob
    output = sum( choices(delt
    # Then [a,b] ->    [a,b+1] if a = 2*layer
    #            ->    [a+1,b] if b = 2*layer
    #            ->  50% chance of [a+1,b] or [a,b+1] otherwise
    # Have delta > 0 "moves" to make
    # Want prob that a > Y at end
    listchoices = [ (0,0,1.0) ]
    for _ in range(delta):
        new_choices = []
        for pair in listchoices:
            if pair[0] == layer + layer:
                new_choices.append( (pair[0], pair[1]+1, pair[2]) )
            elif pair[1] == layer + layer:
                new_choices.append( (pair[0]+1, pair[1], pair[2]) )
            else:
                new_choices.append( (pair[0]+1, pair[1], pair[2]/2) )
                new_choices.append( (pair[0], pair[1]+1, pair[2]/2) )
        listchoices = merge(new_choices)
    output = 0.0
    for choice in listchoices:
        if choice[0] > Y:
            output += choice[2]
    return output

num_cases = int(input())
for case in range(1, num_cases+1):
    N, X, Y = [int(x) for x in input().split()]
    
    layer = find_layer(N)
    if not ( layer*(layer+layer-1) < N and N <= (layer + 1)*(layer + layer + 1) ):
        raise Exception("Failure to find layer.")
    
    if X < 0:
        X = -X
    if ( X + Y ) % 2 == 1:
        output = 0.0
    else:
        XYlayer = (X + Y) // 2
        if XYlayer < layer:
            output = 1.0
        elif XYlayer > layer:
            output = 0.0
        else:
            if N == (layer + 1)*(layer + layer + 1):
                output = 1.0
            else:
                if X == 0:
                    output = 0.0 # N hasn't filled up the layer
                else:
                    delta = N - layer*(layer+layer-1)
                    if Y > delta:
                        output = 0.0
                    else:
                        output = calc_prob(layer, Y, delta)

    print("Case #{}: {:.7}".format(case, output))