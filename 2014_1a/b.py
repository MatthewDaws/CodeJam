# -*- coding: utf-8 -*-
def find_size_cost(tree, root):
    """Input is a rooted tree, represented by tree, which is a dictionary with
    tree[node] = list(children of node)
    and root is the root of the subtree of interest.
    Returns (size, cost) where size is the total size of the subtree, and cost
    is the minimal number of nodes to remove to make the rooted subtree a full
    binary tree."""
    if len( tree[root] ) == 0:
        return (1,0)
    if len( tree[root] ) == 1:
        size, _ = find_size_cost(tree, tree[root][0])
        return (size + 1, size)
    sizes, costs = [], []
    for node in tree[root]:
        s, c = find_size_cost(tree, node)
        sizes.append(s)
        costs.append(c)
    size = 1 + sum(sizes)
    costs = [c - s for c, s in zip(costs, sizes)]
    costs.sort()
    cost = sum(sizes) + costs[0] + costs[1]
    return (size, cost)

# We run into recursion depth problems.  But notice that we can instead use
# a "dynamic programming" style attack: if we work backwards from the leaves
# then we (i) don't use recursion, and (ii) still only visit each node once
def find_size_cost_norec(tree, root):
    tovisit = [root]
    all_nodes = []
    while tovisit:
        node = tovisit.pop()
        all_nodes.append(node)
        tovisit.extend(tree[node])
    # So now all_nodes contains a list of all the nodes in the subtree, with
    # i a child of j implying that i occurs before j in the list
    sizes = dict()
    costs = dict()
    while all_nodes:
        node = all_nodes.pop()
        if len(tree[node]) == 0:
            sizes[node] = 1
            costs[node] = 0
        elif len(tree[node]) == 1:
            sizes[node] = 1 + sizes[tree[node][0]]
            costs[node] = sizes[tree[node][0]]
        else:
            sizes[node] = 1 + sum( sizes[child] for child in tree[node] )
            costs_sub = [costs[child] - sizes[child] for child in tree[node]]
            costs_sub.sort()
            costs[node] = sizes[node] - 1 + costs_sub[0] + costs_sub[1]
    return sizes[root], costs[root]

def make_rooted_tree(edges, root):
    """edges is a list of edges and root is the root vertex
    returns a dictionary tree = dict( node : list(children of node) )"""
    neighbours = dict()
    for e in edges:
        if e[0] not in neighbours:
            neighbours[ e[0] ] = list()
        neighbours[ e[0] ].append( e[1] )
        if e[1] not in neighbours:
            neighbours[ e[1] ] = list()
        neighbours[ e[1] ].append( e[0] )
    tree = dict()
    tovisit = [root]
    visited = set()
    while tovisit:
        node = tovisit.pop()
        visited.add(node)
        tree[node] = list()
        for child in neighbours[node]:
            if child not in visited:
                tree[node].append(child)
                tovisit.append(child)
    return tree

num_cases = int(input())
for case in range(1, num_cases+1):
    num_nodes = int(input())
    edges = [[int(x) for x in input().split()] for _ in range(num_nodes-1)]
    costs = []
    for root in range(1, num_nodes+1):
        size, cost = find_size_cost_norec(make_rooted_tree(edges, root), root)
        costs.append(cost)
    print("Case #{}: {}".format(case, min(costs)))
