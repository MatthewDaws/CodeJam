import math

num_cases = int(input())

for case in range(1,num_cases+1):
    C, F, X = [float(x) for x in input().split()]
    N = math.ceil(X/C - 2/F - 1)
    if N < 1:
        output = X/2
    else:
        T = ( C/(2+n*F) for n in range(N-1, -1, -1) )
        output = sum(T) + X/(2+N*F)
    print("Case #{}: {:.7f}".format(case, output))
