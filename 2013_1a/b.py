# -*- coding: utf-8 -*-
import math
import itertools
from collections import namedtuple

Interval = namedtuple("Interval", ["start", "end", "E0", "F"])

num_cases = int(input())

for case in range(1, num_cases+1):
    E, R, N = [int(x) for x in input().split()]
    v = [int(x) for x in input().split()]

    intervals_to_do = [ Interval(1,N,E,0) ]
    energy = [-1] * N
    running_energy = [E] + [-1] * N
    running_energy_index = 1 # Means we need to compute this
    while len(intervals_to_do) > 0:
        interval = intervals_to_do.pop()
        if interval.start > interval.end:
            continue
        #print("-->", interval)
        if interval.E0 == -1:
            # Should have fixed e1 up to ek for all needed by now
            while running_energy_index <= interval.start - 1:
                if ( running_energy[running_energy_index - 1] == -1 or
                    energy[running_energy_index - 1] == -1 ):
                    raise Exception("Running Energy computation failed.")
                running_energy[running_energy_index] = ( running_energy[running_energy_index - 1]
                    - energy[running_energy_index - 1] + R )
                running_energy_index += 1
            interval = Interval(interval.start, interval.end,
                running_energy[interval.start-1], interval.F)
        vrange = [v[i] for i in range(interval.start-1, interval.end)]
        best_index = interval.start + vrange.index(max(vrange))
        ek = min(E, interval.E0 + (best_index - interval.start) * R)
        delta = interval.F - (interval.end - best_index + 1) * R
        if delta > 0:
            ek -= delta
            if ek < 0:
                raise Exception("Got negative energy!")
            intervals_to_do.append(Interval(best_index + 1, interval.end, -1, interval.F))
            intervals_to_do.append(Interval(interval.start, best_index - 1, interval.E0, ek + delta))
        else:
            intervals_to_do.append(Interval(best_index + 1, interval.end, -1, interval.F))
            intervals_to_do.append(Interval(interval.start, best_index - 1, interval.E0, ek))
        energy[best_index - 1] = ek

    #print("E={}, R={}, v={}".format(str(E), str(R), str(v)))
    #print("ei:", energy)
    #print("Ei:", running_energy)
    output = sum(e * vi for e, vi in zip(energy, v))

    print("Case #{}: {}".format(case, output))
