# -*- coding: utf-8 -*-

import itertools
def choices(N, M):
    """General x = [x2 ... xM] where we have x2 lots of 2, x3 lots of 3,
    and so on.  So 0 <= x2 and \sum xi = N"""
    #yield from itertools.combinations(range(2, M+1), N)
    # Use stars and bars method
    allbars = itertools.combinations( range(1,N+M-1), M-2 )
    for bars in allbars:
        bars = [0] + list(bars) + [N+M-1]
        yi = [ y-x for x, y in zip(bars, bars[1:]) ]
        yield [ y-1 for y in yi ]

import math

from collections import namedtuple
ProdFreqPair = namedtuple("ProdFreqPair", ["product", "freq"])

def prodgreqs_base(A):
    """Given A = [x2 ... xM] where set A contains x2 lots of 2, x3 lots of 3, etc.
    Yields all ProdFreqPair's
    This algorithm does _not_ ensure that the products returned are distinct..."""
    choices = [ list(range(xi+1)) for xi in A ]
    M = len(choices) + 1
    for yi in itertools.product(*choices):
        prod, freq = 1, 1
        for a, y, x in zip(range(2, M+1), yi, A):
            prod *= a ** y
            freq *= math.factorial(x) // math.factorial(y) // math.factorial(x-y)
        yield ProdFreqPair(prod, freq)
            
def prodgreqs(A):
    """Corrects the above by merging entries."""
    pairs = list(prodgreqs_base(A))
    pairs.sort(key = lambda pfp : pfp.product)
    current_prod = -1
    current_freq = 0
    for pfp in pairs:
        if current_prod == -1:
            current_prod = pfp.product
            current_freq = pfp.freq
        else:
            if current_prod == pfp.product:
                current_freq += pfp.freq
            else:
                yield ProdFreqPair(current_prod, current_freq)
                current_prod = pfp.product
                current_freq = pfp.freq
    yield ProdFreqPair(current_prod, current_freq)
            
def probability_all_products(N, M):
    """Returns dictionary prod : pairs (A, f) where A is possible A set, and f is relative frequency of seeing
    this product for this A."""
    Achoices = list( choices(N, M) )
    products = dict()
    for A in Achoices:
        for pfp in prodgreqs(A):
            if pfp.product not in products:
                products[pfp.product] = []
            products[pfp.product].append( (tuple(A), pfp.freq) )
    return products

def probability(prods, prod_dict_As, count_dict):
    """prods = list of products.
    Returns list of tuples (A, count) where A is a possible set, and count is the realtive change of seeing A."""
    for p in prods:
        if p not in prod_dict_As:
            raise Exception("Think we cannot make the product {}.".format(p))
    # Argh, Python, this is a reference!
    #possible_As = prod_dict_As[prods[0]]
    possible_As = set( prod_dict_As[prods[0]] )
    for p in prods[1:]:
        possible_As &= prod_dict_As[p]
    ret = []
    for A in possible_As:
        count = 1
        for p in prods:
            count *= count_dict[(p,A)]
        ret.append((A,count))
    return ret

def probability_A(A):
    N = sum(A)
    p = math.factorial(N)
    for x in A:
        p //= math.factorial(x)
    return p

def solve(prods, prod_dict_As, count_dict):
    probs = probability(prods, prod_dict_As, count_dict)
    # Correct for chance of each A
    probs = [ (A, freq * probability_A(A)) for A, freq in probs ]
    bestA = max(probs, key = lambda pair: pair[1])
    return bestA[0]

import sys

num_cases = int(input())

for case in range(1, num_cases+1):
    R, N, M, K = [int(x) for x in input().split()]

    # prod_dict[p] = list if pairs (A,count) where A can give product p
    #                in count different ways
    print("Building tables...", file=sys.stderr)
    prod_dict = probability_all_products(N, M)
    prod_dict_As = { p : set( A for A, freq in prod_dict[p] ) for p in prod_dict }
    count_dict = dict()
    for p in prod_dict:
        for A, freq in prod_dict[p]:
            count_dict[ (p,A) ] = freq

    output = []
    for r in range(R):
        prods = [int(x) for x in input().split()]
        #print("Solving", prods, file=sys.stderr)
        bestA = solve(prods, prod_dict_As, count_dict)
        output.append( "".join(str(n)*x for n, x in zip(range(2,M+1),bestA)) )

    print("Case #{}:".format(case))
    for s in output:
        print(s)

