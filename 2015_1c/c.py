def solve_fast(C, D, V):
    not_used = D[:]
    not_used.sort()
    max_can_do = 0
    added = []
    while max_can_do < V:
        if max_can_do + 1 in not_used:
            not_used.remove( max_can_do + 1 )
        else:
            added.append(max_can_do + 1)
        # Can make 0 ... max_can_do and max_can_do+1, 2*(max_can_do+1), ..., C*(max_can_do+1)
        # Together means can now make C*max_can_do + C + max_can_do
        max_can_do += C * (max_can_do + 1)
        # If k in not_used then can also now make k, k+1, ..., k + max_can_do
        #   and 2*k, ..., 2*k + max_can_do etc.
        # If k > max_can_do then we'll consider in the future
        # If k <= max_can_do then k + max_can_do >= 2*k and so we get the whole interval
        # up to C*k + max_can_do
        index = 0
        while index < len(not_used):
            if not_used[index] <= max_can_do:
                max_can_do += C * not_used[index]
                del not_used[index]
            else:
                index += 1
    return len(added)

num_cases = int(input())
for case in range(1, num_cases+1):
    C, num_D, V = [int(x) for x in input().split()]
    D = [int(x) for x in input().split()]
    print("Case #{}: {}".format(case, solve_fast(C,D,V)))
