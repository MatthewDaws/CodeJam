num_cases = int( input() )
for case in range(1, num_cases+1):
    length = int( input() )
    x = [int(t) for t in input().split()]
    y = [int(t) for t in input().split()]
    x.sort() # x now increasing
    y.sort(reverse=True) # y now decreasing
    ip = sum(a*b for a, b in zip(x,y))
    print("Case #{}: {}".format(case, ip))
