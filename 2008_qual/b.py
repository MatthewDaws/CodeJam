def time_to_mins(time):
    hours, mins = [int(x) for x in time.split(":")]
    return hours * 60 + mins

from collections import namedtuple
Node = namedtuple("Node", ["index", "station"])

def get_dep(node):
    if node.station=="a":
        return times_a[node.index]
    return times_b[node.index]

num_cases = int( input() )
for case in range(num_cases):
    turn_around_time = int( input() )
    num_a, num_b = [int(x) for x in input().split()]
    times_a = [tuple(time_to_mins(x) for x in input().split()) for _ in range(num_a)]
    times_a.sort(key = lambda pair : pair[1])
    times_a.sort(key = lambda pair : pair[0])
    times_b = [tuple(time_to_mins(x) for x in input().split()) for _ in range(num_b)]
    times_b.sort(key = lambda pair : pair[1])
    times_b.sort(key = lambda pair : pair[0])
    
    # Identify "nodes" by (index, "a") or (index, "b")
    edges = []
    for index, (dep, arr) in enumerate(times_a):
        links = [Node(i,"b") for i, pair in enumerate(times_b) if pair[0] >= arr + turn_around_time]
        edges.append( (Node(index,"a"), links) )
    for index, (dep, arr) in enumerate(times_b):
        links = [Node(i,"a") for i, pair in enumerate(times_a) if pair[0] >= arr + turn_around_time]
        edges.append( (Node(index,"b"), links) )
    """
    if case == 8:
        for n, l in edges:
            print(n, end=" ")
            if n.station=="a":
                print(times_a[n.index], end=" ")
            else:
                print(times_b[n.index], end=" ")
            if len(l)>0:
                print(l[0], end=" ")
            print()
    """
    edges.sort(key = lambda pair : get_dep(pair[0]))
    visited = []
    acount = 0
    bcount = 0
    for node, links in edges:
        if node not in visited:
            if node.station == "a":
                acount += 1
            else:
                bcount += 1
        # Walk down links and find first available not in visited.
        for ld in links:
            if ld not in visited:
                visited.append(ld)
                break

    print("Case #{}: {} {}".format(case+1, acount, bcount))