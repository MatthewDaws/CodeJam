# -*- coding: utf-8 -*-

import math, fractions

from collections import namedtuple
Point = namedtuple("Point", ["x", "y"])

atan2replace_magic = 4*(10**7)
atan2replace_magic1 = 10**7

def atan2replace(y, x):
    if y >= 0:
        if x >= 0:
            return fractions.Fraction(y+1, x+1)
        else:
            return atan2replace_magic1 + fractions.Fraction(y+1, abs(x)+1)
    else:
        if x < 0:
            return 2 * atan2replace_magic1 + fractions.Fraction(abs(y)+1, abs(x)+1)
        else:
            return 3 * atan2replace_magic1 + fractions.Fraction(abs(y)+1, abs(x)+1)
    
num_cases = int(input())

for case in range(1, num_cases+1):
    num_trees = int(input())
    trees = [ [int(x) for x in input().split()] for _ in range(num_trees) ]
    trees = [ Point(line[0],line[1]) for line in trees]

    output = []
    for index, tree in enumerate(trees):
        if num_trees - 1 <= 2:
            output.append(0)
            continue
        # angles from tree relative to horizontal x-axis
        angles = [ atan2replace(t.y - tree.y, t.x - tree.x) for i, t in
                    enumerate(trees) if index != i ]
        print(tree, angles)
        angles.sort()
        #if case == 33:
        #print(tree, angles)
        #if case > 33: exit()
        angles2 = [ x + atan2replace_magic for x in angles ]
        angles.extend( angles2 )
        startindex = 0
        endindex = 0
        lengths = []
        while startindex < num_trees - 1:
            # Find smallest endindex with angles[endindex] >= angles[startindex] + math.pi
            while endindex < len(angles) and angles[endindex] < angles[startindex] + math.pi:
                endindex += 1
            lengths.append( endindex - startindex - 1 )
            startindex += 1
        output.append( min(lengths) )

    print("Case #{}:".format(case))
    for x in output:
        print(x)