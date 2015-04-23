# -*- coding: utf-8 -*-

from collections import namedtuple
Point = namedtuple("Point", ["x", "y"])

def is_on_left(one, two, point):
    """Return True if `point` is strictly in the left half-place formed by the line
    from `one` to `two`"""
    return 0 < ( -(two.y - one.y) * (point.x - one.x)
        + (two.x - one.x) * (point.y - one.y) )

num_cases = int(input())

for case in range(1, num_cases+1):
    num_trees = int(input())
    trees = [ [int(x) for x in input().split()] for _ in range(num_trees) ]
    trees = [ Point(line[0],line[1]) for line in trees]
    
    output = []
    for index, tree in enumerate(trees):
        to_consider = []
        for i, t in enumerate(trees):
            if i != index:
                remove_count = sum( is_on_left(t, tree, s) for s in trees ) 
                to_consider.append( remove_count )
        if len(to_consider) == 0:
            output.append(0)
        else:
            output.append(min(to_consider))

    print("Case #{}:".format(case))
    for x in output:
        print(x)