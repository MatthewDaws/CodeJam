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


def is_prime(p):
    if p == 2:
        return True
    if p % 2 == 0:
        return False
    q = 3
    while q*q <= p:
        if p % q == 0:
            return False
        q += 2
    return True

def next_prime(p):
    """Find the next prime greater than p"""
    if p == 1:
        return 2
    p += 1
    if p % 2 == 0:
        p += 1
    while not is_prime(p):
        p += 2
    return p


def Solve1(A, B, P):
    df = DisjointSetForests2()
    for n in range(A, B+1):
        df.AddSet(n)

    p = P - 1
    while p <= B-A:
        p = next_prime(p)
        if A % p == 0:
            first = A
        else:
            first = p + (A//p)*p
        second = p*(B//p)
        if first < second:
            for n in range(first, second+1, p):
                df.Union(first, n)
                
    return len( list(df.Subsets()) )
    return 0

import sys

num_cases = int(input())
for case in range(1, num_cases+1):
    A, B, P = [ int(x) for x in input().split() ]
    print(A,B,P, file=sys.stderr)
    output = Solve1(A,B,P)
    print("Case #{}: {}".format(case, output))
