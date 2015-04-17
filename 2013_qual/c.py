# -*- coding: utf-8 -*-
def is_palindrome(x):
    s = str(x)
    n, i = len(s)-1, 0
    while i < n - i:
        if s[i] != s[n-i]:
            return False
        i += 1
    return True

def check(A,B):
    x = 1
    output = []
    while x*x <= B:
        if A <= x*x and is_palindrome(x) and is_palindrome(x*x):
            output.append(x)
        x += 1
    return output

def find_seqs(length):
    """Yields sequences of `length` consisting of 1 or 2, and
    have sum squares <=4"""
    for num in range(2**length):
        digits = [ 1 + ((num>>k)&1) for k in range(length) ]
        if sum( x*x for x in digits ) <= 4:
            yield digits

def find_indices(length, digits):
    """Yields sequences of `digits` starting with 0, strictly increasing,
    and with maximum <= `length`"""
    seq = list(range(digits))
    if seq[-1] > length:
        return
    while True:
        yield seq[:]
        index = digits - 1
        seq[index] += 1
        while index > 0 and seq[index] > length - (digits - 1 - index):
            index -= 1
            seq[index] += 1
        if index == 0:
            return
        while index < digits - 1 :
            index += 1
            seq[index] = seq[index-1] + 1

def find_below(B):
    """Find x<=10**B (roughly) with x palindromic and x*x palindromic"""
    output = [1,2,3]
    for numdigits in range(1,5):
        for digits in find_seqs(numdigits):
            # Generates all palindromes with number of digits <= 2k+1
            # so want 2k >= B - 1
            for length in range(B//2):
                for indices in find_indices(length, numdigits):
                    digs = [0] * (length+1)
                    for index, digit in zip(indices, digits):
                        digs[index] = digit
                    # Mirror
                    ds = digs + list(reversed(digs))
                    x = sum( (10**n)*val for n, val in enumerate(ds) )
                    output.append(x)
                    # Mirror and add central digit
                    for mid in [0,1,2]:
                        if mid*mid + 2*sum(k*k for k in digs) <= 9:
                            ds = digs + [mid] + list(reversed(digs))
                            x = sum( (10**n)*val for n, val in enumerate(ds) )
                            output.append(x)
    return output

fairsqs = find_below(60)
fairsqs.sort()

num_cases = int(input())
for case in range(1, num_cases+1):
    A, B = [int(x) for x in input().split()]
    output = 0
    for x in fairsqs:
        if x*x > B: break
        if A <= x*x: output += 1
    print("Case #{}: {}".format(case, output))