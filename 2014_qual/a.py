num_cases = int(input())

for case in range(1,num_cases+1):
    row1 = int(input())
    grid1 = [ [int(x) for x in input().split()] for _ in range(4) ]
    row2 = int(input())
    grid2 = [ [int(x) for x in input().split()] for _ in range(4) ]
    set1 = set( grid1[row1-1] )
    set2 = set( grid2[row2-1] )
    possibles = set1 & set2
    if len(possibles) == 1:
        output = next(iter(possibles))
    elif len(possibles) > 1:
        output = "Bad magician!"
    else:
        output = "Volunteer cheated!"
    print("Case #{}: {}".format(case, output))
