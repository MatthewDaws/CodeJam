def solve(r):
    stars = 0
    ratings = [ (x,y,n) for n, (x,y) in enumerate(r) ]
    done1star = [ False ] * len(ratings)
    count = 0
    while len(ratings) > 0:
        #print(stars,"-->")
        #print(ratings)
        count += 1
        # Can we solve a 2 star game now?
        solved2star = False
        for index in range(len(ratings)):
            if ratings[index][1] <= stars:
                if done1star[ ratings[index][2] ]:
                    stars += 1
                else:
                    stars += 2
                del ratings[index]
                solved2star = True
                break
        # Do we need to try 1 star?
        if solved2star:
            continue
        options = [ index for index, rate in enumerate(ratings) if rate[0] <= stars and not done1star[ rate[2] ] ]
        if len(options) == 0:
            return "Too Bad"
        index = max(options, key = lambda index : ratings[index][1])
        stars += 1
        done1star[ ratings[index][2] ] = True
    return count

num_cases = int(input())
for case in range(1, num_cases+1):
    num_games = int(input())
    data = [ [int(x) for x in input().split()] for _ in range(num_games) ]
    print("Case #{}: {}".format(case, solve(data)))