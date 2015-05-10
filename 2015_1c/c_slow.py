import itertools

def gen_all(C, D, V):
    """C = max number of coins of one type
    D = list of demons
    V = maximum to make"""
    poss = set()
    # This is O( (C+1)**D )
    for choice in itertools.product(range(C+1), repeat = len(D)):
        s = sum( c * d for c, d in zip(choice, D) )
        if s <= V:
            poss.add(s)
    return list(poss)

def solve(C, D, V):
    options = [ [] ]
    count = -1
    while len(options) > 0:
        added = options.pop()
        #print("Trying", D+added)
        can_make = gen_all(C, D + added, V)
        can_make.sort()
        done = True
        # STUPID MISTAKE here: need to also check if we can make up V!
        for i, x in enumerate(can_make):
            if x != i:
                # Can't make i but can make 0, ..., i-1
                maybe = set(range(1, i+1))
                maybe = maybe.difference( set(D) )
                maybe = maybe.difference( set(added) )
                for x in maybe:
                    options.append( added + [x] )
                done = False
                break
        if done and max(can_make) < V:
            i = max(can_make) + 1
            maybe = set(range(1, i+1))
            maybe = maybe.difference( set(D) )
            maybe = maybe.difference( set(added) )
            for x in maybe:
                options.append( added + [x] )
            done = False
        if done:
            if count == -1 or len(added) < count:
                count = len(added)
    return count

# Know C==1 so brute-force...
def brute(D, V):
    count = -1
    options = [ [] ]
    while len(options) > 0:
        added = options.pop()
        if count != -1 and len(added) >= count:
            continue
        #print("Trying...",added)
        canmake = gen_all(1, D + added, V)
        if len(canmake) != V + 1:
            toadd = set(range(1, V+1))
            toadd.difference_update( D )
            toadd.difference_update( added )
            toadd = list(toadd)
            toadd.sort(reverse = True)
            for x in toadd:
                options.append( added + [x] )
        else:
            if count == -1 or len(added) < count:
                count = len(added)
                #print(count, added)
    return count    

def solve_better(C, D, V):
    added = []
    while True:
        can_make = gen_all(C, D + added, V)
        want = set(range(V+1))
        want.difference_update(can_make)
        if len(want) == 0:
            return len(added)
        added.append( min(want) )

num_cases = int(input())
for case in range(1, num_cases+1):
    C, num_D, V = [int(x) for x in input().split()]
    D = [int(x) for x in input().split()]
    #if brute(D, V) != solve(C,D,V):
    #    print(C,D,V)
    #    exit()
    print("Case #{}: {}".format(case, solve_better(C,D,V)))
