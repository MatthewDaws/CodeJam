num_cases = int(input())
for case in range(1, num_cases+1):
    R, C, W = [int(x) for x in input().split()]
    n = C // W
    count = (R - 1) * n
    if n * W  == C:
        count += n + W - 1
    else:
        count += n + W

    print("Case #{}: {}".format(case, count))