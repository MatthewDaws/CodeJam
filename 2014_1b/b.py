from collections import namedtuple
Entry = namedtuple("Entry", ["A","B","K"])
from collections import defaultdict

def combs_dynamic(A, B, K):
    if A == 0 or B == 0 or K == 0:
        return 0
    tofind = defaultdict(int)
    tofind[Entry(A,B,K)] = 1
    while True:
        #print(tofind)
        # Find entry with biggest B
        allB = list(tofind)
        allB.sort(key = lambda e : min(e.A,e.B))
        entry = allB.pop()
        if min(entry.A, entry.B) == 1:
            break # At end now
        count = tofind[entry]
        del tofind[entry]
        newentry = Entry((entry.A+1)//2, (entry.B+1)//2, (entry.K+1)//2)
        tofind[newentry] += count
        newentry = Entry((entry.A)//2, (entry.B+1)//2, (entry.K+1)//2)
        tofind[newentry] += count
        newentry = Entry((entry.A+1)//2, (entry.B)//2, (entry.K+1)//2)
        tofind[newentry] += count
        newentry = Entry((entry.A)//2, (entry.B)//2, (entry.K)//2)
        tofind[newentry] += count
    # Now need to sum and return
    count = 0
    for entry in tofind:
        if entry.A == 0 or entry.B == 0 or entry.K == 0:
            pass
        else:
            if entry.A == 1:
                count += entry.B * tofind[entry]
            elif entry.B == 1:
                count += entry.A * tofind[entry]
            else:
                raise Exception("Odd: "+str(entry))
    return count

num_cases = int(input())
for case in range(1, num_cases+1):
    A, B, K = [int(x) for x in input().split()]
    print("Case #{}: {}".format(case, combs_dynamic(A,B,K)))
