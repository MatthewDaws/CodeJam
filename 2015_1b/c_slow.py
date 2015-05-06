import sys

from collections import namedtuple
Group = namedtuple("Group", ["degree", "hikers", "minutes"])

def cost_zeros(time, zero_hikers):
    count = 0    
    for g in zero_hikers:
        for k in range(g.hikers):
            min = (g.minutes + k) * 360
            count += max(1, time // min)
    return count

def cost_nonzeros(time, nons):
    """Assume non_zero_hikers sorted by "offset".
    Returns (crude lower bound, count)."""
    lower, cost = 0, 0
    for (min, offset) in nons:
        if time < offset:
            cost += 1
        else:
            cost += (time - offset) // min
            # If `time` increases then so will this.
            lower += (time - offset) // min
    return lower, cost

num_cases = int(input())
for case in range(1, num_cases+1):
    N = int(input())
    hikers = [ (int(x) for x in input().split()) for _ in range(N) ]
    hikers = [Group(D,H,M) for (D,H,M) in hikers]
    
    # Find those with 0 degrees and those with non-zero degree
    # Actually, if we read the problem correctly, then zeros will always
    # be empty!
    zeros = [ g for g in hikers if g.degree == 0 ]
    nonzeros = [ g for g in hikers if g.degree != 0 ]
    # (min, offset) pairs
    nons = [ ((g.minutes + k) * 360, (360 - g.degree) * (g.minutes + k))
                for g in nonzeros for k in range(g.hikers) ]
    nons.sort(key = lambda pair : pair[1])
    
    best = cost_zeros(0, zeros)
    _, cost = cost_nonzeros(0, nons)
    best += cost
    print(best)
    for _, time in nons:
        count = cost_zeros(time, zeros)
        lower, cost = cost_nonzeros(time, nons)
        print(count + lower, count + cost)
        if count + lower >= best:
            break
        best = min(best, count + cost)

    print("Case #{}: {}".format(case, best))
