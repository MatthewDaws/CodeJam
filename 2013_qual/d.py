from collections import namedtuple
from collections import Counter
Chest = namedtuple("Chest", ["open", "contains"])

def have_enough_keys(chests, keys):
    """chests: list of Chest tuples
    keys: list of keys we have
    Counts all keys in total and checks that in total, we have more keys of each type than chests."""
    have = Counter(keys)
    for chest in chests:
        have.update( chest.contains )
    needed = Counter( chest.open for chest in chests )
    return all( needed[key] <= have[key] for key in needed )

def not_enough_keys(chests, keys):
    """Returns a list of key types where we don't current have enough to open all chests of that type."""
    have = Counter(keys)
    needed = Counter( chest.open for chest in chests )
    return [ key for key in needed if needed[key] > have[key] ]

def all_paths(chests, keys):
    """Checks that for each key type where we currently don't have enough to open all chests, there is
    a path from a key we have to a key of that type."""
    not_enough = not_enough_keys(chests, keys)
    for key in not_enough:
        indices_to_consider = set( index for index, chest in enumerate(chests) if key in chest.contains )
        foundone = False
        while True:
            keys_want = set( chests[i].open for i in indices_to_consider )
            if len( keys_want & set(keys) ) > 0:
                foundone = True
                break
            new_indices = set( index for index, chest in enumerate(chests)
                            if len( keys_want & set( chest.contains ) ) > 0 )
            oldlen = len(indices_to_consider)
            indices_to_consider = indices_to_consider | new_indices
            if len(indices_to_consider) == oldlen:
                break
        if not foundone:
            return False
    return True

def can_solve(chests, keys):
    return have_enough_keys(chests, keys) and all_paths(chests, keys)

num_cases = int(input())
for case in range(1, num_cases+1):
    num_start_keys, num_chests = [int(x) for x in input().split()]
    keys = [int(x) for x in input().split()]
    chests = []
    for _ in range(num_chests):
        data = [int(x) for x in input().split()]
        chests.append( Chest(data[0], data[2:]) )

    if not have_enough_keys(chests, keys):
        output = "IMPOSSIBLE"
    else:

        index_to_chests = [x+1 for x in range(num_chests)]
        ordering = []
        while len(index_to_chests) > 0:
            indices = [ index for index, chest in enumerate(chests) if chest.open in keys ]
            for index in indices:
                chestnum = index_to_chests[index]
                new_chests = chests[:]
                new_keys = keys[:]
                new_keys.extend( chests[index].contains )
                del new_chests[index]
                new_keys.remove(chests[index].open)
                shortcut = ( len(ordering) > 0 and len(indices) == 1 )
                if shortcut or all_paths(new_chests, new_keys):
                    ordering.append( chestnum )
                    del index_to_chests[index]
                    chests, keys = new_chests, new_keys
                    break
            if len(ordering) == 0: # Impossible?
                break
            #print(case, "-->", ordering)
    
        if len(ordering) == 0:
            output = "IMPOSSIBLE"
        else:
            output = " ".join(str(x) for x in ordering)

    print("Case #{}: {}".format(case, output))
