# -*- coding: utf-8 -*-

def prime_list(upto):
    """Returns a list of primes up to `upto` inclusive"""
    if upto < 2: return []
    # Mapping will be 0->3, 1->5, 2->7 etc.  n->n+n+3
    length = upto
    sieve = [True] * ((length - 1)//2)
    current_prime = 3
    while current_prime*current_prime <= length:
        p = current_prime * current_prime
        while p <= length:
            sieve[(p-3)//2] = False
            p += current_prime * 2 # Skip evens!
        current_prime += 2
        while current_prime*current_prime < length and sieve[(current_prime-3)//2] == False:
            current_prime += 2
            
    primes = []
    primes.append(2)
    #current_prime = 3
    #while current_prime <= length:
    #    if sieve[(current_prime-3)//2]:
    #        primes.append(current_prime)
    #    current_prime += 2
    primes.extend( cp+cp+3 for cp in range(0, (length-1)//2) if sieve[cp] )
    return primes

primes_length = 0
primes = []

def Solve(A, B, P):
    # Setup prime list
    global primes_length
    global primes
    if B - A > primes_length:
        primes_length = B - A
        print("Rebuilding prime list ->", primes_length, file=sys.stderr)
        primes = prime_list(primes_length)

    # Find P in primes
    if P > B - A:
        return B - A + 1
    prime_index = 0
    while prime_index < len(primes) and primes[prime_index] < P:
        prime_index += 1
    if prime_index == len(primes):
        return B - A + 1

    # Find sets X_p
    # We only want those p with len(X_p) >= 2 and a list of those
    # numbers not in any such p
    Xplist = []
    inanXp = [False] * (B-A+1)
    while prime_index < len(primes):
        p = primes[prime_index]
        prime_index += 1
        if A % p == 0:
            first = A
        else:
            first = p + (A//p)*p
        second = p*(B//p)
        if first < second:
            Xplist.append(p)
            for x in range(first, second+1, p):
                inanXp[x - A] = True

    if len(Xplist) == 0:
        return B - A + 1

    print("Graph has", len(Xplist), "nodes.", file=sys.stderr)
    neighbours = []
    for p in Xplist:
        neighbours.append( [ q for q in Xplist if p != q and B % (p*q) <= B - A ] )
    print("Number of edges:", sum(len(n) for n in neighbours), file=sys.stderr)

    # Construct graph: Xp is linked to Xq if and only if B % (p*q) <= B - A
    component = [0] * len(Xplist)
    current_component = 1
    while True:
        try:
            index = next( index for index, com in enumerate(component) if com==0 )
        except StopIteration:
            break
        # So index will be the base of the next component
        tovisit = [index]
        while len(tovisit) > 0:
            node = tovisit.pop()
            component[node] = current_component
            # Find unvisited neighbours of node
            for index, com in enumerate(component):
                if com == 0 and B % (Xplist[index] * Xplist[node]) <= B - A:
                    tovisit.append(index)
        current_component += 1

    # Return
    singletons_count = 0
    for x in inanXp:
        if not x:
            singletons_count += 1
    return singletons_count + max(component)

import sys

num_cases = int(input())
for case in range(1, num_cases+1):
    A, B, P = [ int(x) for x in input().split() ]
    print(A,B,P, file=sys.stderr)
    output = Solve(A,B,P)
    print("Case #{}: {}".format(case, output))
