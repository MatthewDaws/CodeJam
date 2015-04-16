# -*- coding: utf-8 -*-
class DisjointSetForests2:
    def __init__(self):
        self.parents = dict()
    
    def AddSet(self, value):
        """Add a singleton set {value}."""
        self.parents[value] = value
    
    def Find(self, node):
        """Returns a 'representative' of the subset containing `node`.  This representative will not
        change until a call to Union.
        So `n1` and `n2` are in the same set if and only if Find(n1) == Find(n2)"""
        # Implements path compression
        # Common cases first
        if self.parents[node] == node:
            return node
        n = self.parents[node]
        if self.parents[n] == n:
            return n
        current_path = [node]
        while self.parents[n] != n:
            current_path.append(n)
            n = self.parents[n]
        # n is now the root and our 'representative'
        for m in current_path: # Compress path
            self.parents[m] = n
        return n
    
    def Union(self, n1, n2):
        """Union the two sets which contain n1 and n2."""
        rep1 = self.Find(n1)
        rep2 = self.Find(n2)
        if rep1 != rep2:
            self.parents[rep2] = rep1
            
    def Subsets(self):
        """Returns an iterable giving exactly one 'representative' for each subset."""
        return ( value for value, parent in self.parents.items() if value == parent )
    
    
    def __repr__(self):
        reps = self.Subsets()
        strings = []
        for r in reps:
            s = ", ".join( str(value) for value in self.parents.keys() if self.Find(value)==r )
            strings.append("{ "+s+" }")
        return "DisjointSetForests: " + " ".join(strings)

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


def Solve1(A, B, P):
    df = DisjointSetForests2()
    for n in range(A, B+1):
        df.AddSet(n)

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

    while prime_index < len(primes) and primes[prime_index] <= B-A:
        p = primes[prime_index]
        prime_index += 1
        if A % p == 0:
            first = A
        else:
            first = p + (A//p)*p
        second = p*(B//p)
        if first < second:
            for n in range(first, second+1, p):
                df.Union(first, n)
                
    return len( list(df.Subsets()) )

import sys

num_cases = int(input())
for case in range(1, num_cases+1):
    A, B, P = [ int(x) for x in input().split() ]
    print(A,B,P, file=sys.stderr)
    output = Solve1(A,B,P)
    print("Case #{}: {}".format(case, output))
