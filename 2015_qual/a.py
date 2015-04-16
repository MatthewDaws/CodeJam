num_cases = int(input())

for case in range(1, num_cases+1):
    Smax, Si = input().split()
    Smax = int(Smax)
    Si = [int(x) for x in Si]
    #print(Smax, Si)

    looking_at = 0
    standing = 0
    extras = 0
    while looking_at < Smax:
        standing += Si[looking_at]
        looking_at += 1
        if standing < looking_at:
            extras += 1
            standing += 1

    output = extras
    print("Case #{}: {}".format(case, output))
