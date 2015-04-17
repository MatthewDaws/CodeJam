from collections import namedtuple
Partial = namedtuple("Partial", ["partial_mask", "Asets", "Bsets"])

def find_solutions(outlets, devices):
    N = len(outlets)
    L = len(outlets[0])

    solutions = []
    totry = [Partial([], [list(range(N))], [list(range(N))])]
    while totry:
        partial = totry.pop()
        current_bit = len(partial.partial_mask)
        if current_bit == L:
            solutions.append( partial.partial_mask[:] )
            continue
    
        for newbit in range(2):
            new_mask = partial.partial_mask[:]
            new_mask.append(newbit)
            newAsets = []
            newBsets = []
            coherent = True
            for index in range(len(partial.Asets)):
                A, B = partial.Asets[index], partial.Bsets[index]
                zeros = [x for x in A if outlets[x][current_bit] == 0]
                zerosc = [x for x in A if outlets[x][current_bit] == 1]
                match = [x for x in B if devices[x][current_bit] ^ newbit == 0]
                matchc = [x for x in B if devices[x][current_bit] ^ newbit == 1]
                if len(zeros) == len(match):
                    if len(zeros) > 0:
                        newAsets.append(zeros)
                        newBsets.append(match)
                    if len(zerosc) > 0:
                        newAsets.append(zerosc)
                        newBsets.append(matchc)
                else:
                    coherent = False
                    break
            if coherent:
                totry.append( Partial(new_mask, newAsets, newBsets) )
    return solutions

num_cases = int(input())
for case in range(1,num_cases+1):
    N, L = [int(x) for x in input().split()]
    outlets = [ [ int(x) for x in bits ] for bits in input().split() ]
    devices = [ [ int(x) for x in bits ] for bits in input().split() ]
    solns = find_solutions(outlets, devices)
    if len(solns) > 0:
        output = min( sum(x) for x in solns )
    else:
        output = "NOT POSSIBLE"
    print("Case #{}: {}".format(case, output))
