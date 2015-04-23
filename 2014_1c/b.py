# -*- coding: utf-8 -*-
import math

def checkletter(string, alpha):
    first = string.index(alpha)
    last = string.rindex(alpha)
    sub = string[first:last+1]
    if sub != alpha * len(sub):
        return False
    return True
    
def check(string):
    letters = set(string)
    return all( checkletter(string, alpha) for alpha in letters )

import itertools
def brute_force(data):
    return sum( check("".join(perm)) for perm in itertools.permutations(data) )

def reduce_to_singles(iterable):
    iterator = iter(iterable)
    current = next(iterator)
    for x in iterator:
        if x != current:
            yield current
            current = x
    yield current

num_cases = int(input())
for case in range(1, num_cases+1):
    N = int(input())
    data = [x for x in input().split()]

    data = ["".join(reduce_to_singles(x)) for x in data]
    letters = set()
    for x in data:
        letters |= set(x)

    count = 1
    for alpha in letters: #"abcdefghijklmnopqrstuvwxyz":
        alphastrings = []
        otherstrings = []
        for x in data:
            if alpha in x:
                alphastrings.append(x)
            else:
                otherstrings.append(x)
        if len(alphastrings) == 0:
            data = otherstrings
        elif len(alphastrings) == 1:
            if not checkletter(alphastrings[0], alpha):
                count = 0
                break
            data = alphastrings + otherstrings
        else:
            # Those string which contain more than just alpha
            ofinterest = [x for x in alphastrings if x != alpha*len(x)]
            if len(ofinterest) > 2:
                count = 0
                break
            elif len(ofinterest) == 2:
                if not checkletter(ofinterest[0], alpha) or not checkletter(ofinterest[1], alpha):
                    count = 0
                    break
                if ofinterest[0][0] == alpha: # first string starts with alpha
                    if ofinterest[1][-1] == alpha:
                        data = [ofinterest[1] + ofinterest[0]]
                    else:
                        count = 0 # 2nd string doesn't end with alpha
                        break
                elif ofinterest[0][-1] == alpha: # first string ends with alpha
                    if ofinterest[1][0] == alpha:
                        data = [ofinterest[0] + ofinterest[1]]
                    else:
                        count = 0 # 2nd string doesn't start with alpha
                        break
                else:
                    count = 0 # alpha in middle of first string
                    break
                count *= math.factorial(len(alphastrings) - 2)
            elif len(ofinterest) == 1:
                if not checkletter(ofinterest[0], alpha):
                    count = 0
                    break
                if ofinterest[0][0] == alpha or ofinterest[0][-1] == alpha:
                    data = [ofinterest[0]]
                    count *= math.factorial(len(alphastrings) - 1)
                else:
                    count = 0 # alpha in middle of string
                    break
            else:
                count *= math.factorial(len(alphastrings))
                data = [alpha]
            data.extend(otherstrings)

    count *= math.factorial(len(data))

    print("Case #{}: {}".format(case, count % 1000000007))
