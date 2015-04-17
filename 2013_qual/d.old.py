from collections import namedtuple
Chest = namedtuple("Chest", ["open", "contains"])

class Problem:
    def __init__(self, startkeys, chests)
        self.keys = startkeys[:]
        self.chests = chests[:]

    def clone(self):
        return Problem(self.keys, self.chests)

    def open_chest(self, index):
        self.keys.remove(self.chests[index].open)
        self.keys.extend(self.chests[index].contains)
        del self.chests[index]

    def is_done(self):
        return len(self.chests) == 0

    def open_all(self):
        """If have N chests needing key type k and >=N keys of that type then open all chests"""
        opened = True
        while opened:
            opened = False
            keyshave = set( self.keys )
            for key in keyshave:
                numberhave = sum( k == key for k in self.keys )
                numberneeded = sum( chest.open == key for chest in self.chests )
                if numberhave >= numberneeded:
                    index = 0
                    while index < len(self.chests):
                        if self.chests[index].open == key:
                            self.open_chest(index) # Modifies self.chests  !!
                        else:
                            index += 1
                    opened = True
                    break

    def do_chain(self, length):
        """Returns True if there is a "chain" of `length`, which is also performed."""
        

num_cases = int(input())
for case in range(1, num_cases+1):
    num_start_keys, num_chests = [int(x) for x in input().split()]
    start_keys = [int(x) for x in input().split()]
    chests = []
    for _ in range(num_chests):
        data = [int(x) for x in input().split()]
        chests.append( Chest(data[0], data[2:]) )
    


    print("Case #{}: {}".format(case, output))
