import math
num_cases = int(input())

for case in range(1, num_cases+1):
    diners = int(input())
    pancakes = [int(x) for x in input().split()]
    #print("--->", pancakes)
    maximum = max(pancakes)
    best = maximum
    for N in range(2,maximum):
        M = sum( math.ceil(x/N) - 1 for x in pancakes )
        if M + N < best:
            best = M + N

    output = best
    print("Case #{}: {}".format(case, output))
