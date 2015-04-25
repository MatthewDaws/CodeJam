# -*- coding: utf-8 -*-



num_cases = int(input())
for case in range(1, num_cases+1):
    armins_size, motes = [int(x) for x in input().split()]
    sizes = [int(x) for x in input().split()]
    
    if armins_size == 1:
        # Can't ever absorb!
        output = len(sizes)
    else:
        sizes.sort()
        
        additions = []
        for size in sizes:
            count = 0
            while armins_size <= size:
                count += 1
                armins_size += armins_size-1
            additions.append(count)
            armins_size += size # Finally can absorb
        # Check if removing makes more sense
        removals = 0
        while len(additions) > 0:
            # Test removing k items
            did_remove = False
            for k in range(1, len(additions)+1):
                if sum(additions[-k:]) > k:
                    removals += k
                    additions = additions[:-k]
                    did_remove = True
                    break
            if not did_remove:
                break

        if len(additions) > 0:
            output = removals + sum(additions)
        else:
            output = removals

    print("Case #{}: {}".format(case, output))