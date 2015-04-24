# -*- coding: utf-8 -*-

import math

from collections import namedtuple
Point = namedtuple("Point", ["x", "y"])

def yield_removals(tree, trees):
    """`tree` is current point of interest, and `trees` is an iterable
    of all the other trees."""
    angles = [ math.atan2(t.y - tree.y, t.x - tree.x) for t in trees ]
    num_trees = len(angles)
    angles.sort()
    angles2 = [ x + 2.0*math.pi for x in angles ]
    angles.extend(angles2)
    startindex = 0
    endindex = 0
    while startindex < num_trees:
        # Find smallest endindex with angles[endindex] >= angles[index] + math.pi
        while endindex < len(angles) and angles[endindex] < angles[startindex] + math.pi - epsilon:
            endindex += 1
        # Don't want to count colinear points
        realstartindex = startindex + 1
        while angles[realstartindex] < angles[startindex] + epsilon:
            realstartindex += 1
        realstartindex -= 1
        # Add in appropriate number to list
        for _ in range(realstartindex - startindex + 1):
           yield ( endindex - realstartindex - 1 )
        # Next loop
        startindex = realstartindex + 1

num_cases = int(input())

for case in range(1, num_cases+1):
    num_trees = int(input())
    trees = [ [int(x) for x in input().split()] for _ in range(num_trees) ]
    trees = [ Point(line[0],line[1]) for line in trees]

    # Worst angle is roughly atan(1e-6) approx 1e-8
    epsilon = 1e-10

    output = []
    for index, tree in enumerate(trees):
        if num_trees - 1 <= 2:
            output.append(0)
        else:
            others = ( t for i, t in enumerate(trees) if i != index )
            output.append( min(yield_removals(tree, others)) )

    print("Case #{}:".format(case))
    for x in output:
        print(x)
