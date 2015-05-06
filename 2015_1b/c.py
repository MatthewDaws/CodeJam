import sys, heapq

from collections import namedtuple
Group = namedtuple("Group", ["degree", "hikers", "minutes"])
Case = namedtuple("Case", ["offset", "min", "count"])

num_cases = int(input())
for casenum in range(1, num_cases+1):
    N = int(input())
    hikers = [ (int(x) for x in input().split()) for _ in range(N) ]
    hikers = [Group(D,H,M) for (D,H,M) in hikers]

    # Move into a format we need
    hikers = [ Case( (360 - g.degree) * (g.minutes + k), (g.minutes + k) * 360, 1 )
                for g in hikers for k in range(g.hikers) ]
    heapq.heapify(hikers)

    cost = len(hikers) # Initial cost at time = 0
    best = cost
    possible_decreases = len(hikers)
    while True:
        # Process all the events at the next time step
        current_time = hikers[0].offset
        while current_time == hikers[0].offset:
            case = heapq.heappop(hikers)
            if case.count == 1:
                cost -= 1
                possible_decreases -= 1
            else:
                cost += 1
            heapq.heappush(hikers, Case(case.offset + case.min, case.min, case.count + 1))
        # Next loop
        best = min(cost, best)
        if cost - possible_decreases >= best:
            break

    print("Case #{}: {}".format(casenum, best))
