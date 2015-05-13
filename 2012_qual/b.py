normals = dict()
for x in range(10):
    normals[3 * x] = x  # (x,x,x)
    normals[3 * x + 1] = x + 1 # (x,x,x+1)
    normals[3 * x + 2] = x + 1  # (x,x+1,x+1)
normals[30] = 10

surprises = dict()
for x in range(9):
    surprises[3 * x + 2] = x + 2  # (x,x,x+2)
    surprises[3 * x + 3] = x + 2  # (x,x+1,x+2)
    surprises[3 * x + 4] = x + 2  # (x,x+2,x+2)

# Notice that surprises[x] is defined for 2 <= x <= 28 and surprises[x] >= normals[x]

num_cases = int(input())
for case in range(1, num_cases+1):
    data = [int(x) for x in input().split()]
    count, num_surprises, at_least = data[0], data[1], data[2]
    data = data[3:]
    
    # For each entry, either:
    #   - normals[x] >= at_least    so count for sure
    #   - x in surprises and surprises[x] < at_least    so can never count
    #   - x not in surprises and normals[x] < at_least   so can never count
    #   - x in surprises and surprises[x] >= at_least    so maybe can count
    # If we don't use all the `count` in the last case, we can just randomly choose
    # some others, as the maximum score will only increase.

    outcount = 0
    possibles = 0
    for x in data:
        if normals[x] >= at_least:
            outcount +=1
        else:
            # normals[x] < at_least
            if x in surprises and surprises[x] >= at_least:
                possibles += 1

    outcount += min(possibles, num_surprises)            

    print("Case #{}: {}".format(case, outcount))
