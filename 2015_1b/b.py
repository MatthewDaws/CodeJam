def odd_alg1(R, C, N):
    to_remove = R * C - N
    saving = 0
    mid_choices = ((R-2) * (C-2) + 1) // 2
    saving += 4 * min(to_remove, mid_choices)
    to_remove -= min(to_remove, mid_choices)
    if to_remove <= 0: return saving
    edge_choices = R + C - 6
    saving += 3 * min(to_remove, edge_choices)
    to_remove -= min(to_remove, edge_choices)
    if to_remove <= 0: return saving
    saving += 2 * min(to_remove, 4)
    to_remove -= min(to_remove, 4)
    if to_remove <= 0: return saving
    return -1 # Can't actually do!

def odd_alg2(R, C, N):
    to_remove = R * C - N
    saving = 0
    mid_choices = ((R-2) * (C-2) - 1) // 2
    saving += 4 * min(to_remove, mid_choices)
    to_remove -= min(to_remove, mid_choices)
    if to_remove <= 0: return saving
    edge_choices = R + C -2
    saving += 3 * min(to_remove, edge_choices)
    to_remove -= min(to_remove, edge_choices)
    if to_remove <= 0: return saving
    return -1

def solve_fast(R, C, N):
    # Various corner cases:
    if N == 0:
        return 0
    if R > C: # Ensure R <= C
        R, C = C, R
    if R == 1:
        if (C % 2) == 0:
            left = N - (C // 2)
            count = 0
            if left <= 0: return count
            left -= 1
            count += 1
            if left <= 0: return count
            return count + 2 * left
        # C odd
        left = N - ((C+1) // 2)
        count = 0
        if left <= 0: return count
        return count + 2 * left
        
    if (R % 2) == 1 and (C % 2) == 1:
        # Both odd algorithm
        left = N - (R * C + 1) // 2
        if left <= 0: return 0
        one = odd_alg1(R, C, N)
        two = odd_alg2(R, C, N)
        if_full = 2*R*C - R - C
        if one == -1:
            if two == -1:
                raise Exception("Arse!")
            return if_full - two
        return if_full - max(one, two)
        
    # One even
    left = N - R * C // 2
    count = 0
    if left <= 0: return count
    count += 2 * min(2, left)
    left -= min(2, left)
    if left <= 0: return count
    count += 3 * min(left, R + C - 4)
    left -= min(left, R + C - 4)
    if left <= 0: return count
    return count + 4 * left

num_cases = int(input())
for case in range(1, num_cases+1):
    R, C, N = [int(x) for x in input().split()]
    output = solve_fast(R, C, N)
    print("Case #{}: {}".format(case, output))
