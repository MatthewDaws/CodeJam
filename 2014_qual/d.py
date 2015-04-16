class Ken:
    def __init__(self, weights):
        self.weights = weights[:]
        self.weights.sort()
        
    def play(self, other_weight):
        """Implements Ken's optimal strategy, based on `other_weight` being played by
        Naomi.  Returns weight which Ken will play."""
        if other_weight > self.weights[-1]:
            # Can't win so play smallest weight
            ken_play = self.weights[0]
            del self.weights[0]
        else:
            # Can win, so play least weight which wins
            index = len(self.weights) - 1
            while index > 0 and self.weights[index - 1] > other_weight:
                index -= 1
            ken_play = self.weights[index]
            del self.weights[index]
        return ken_play
    
def War(kweights, nweights):
    """Returns number of points Ken wins."""
    k = Ken(kweights)
    kwins = 0
    for x in nweights:
        ken_play = k.play(x)
        if ken_play > x:
            kwins += 1
    return kwins

def DWar(kweights, nweights):
    """Return number of points Ken wins in deceitful war."""
    n = nweights[:]
    n.sort() # So n now increasing
    k = Ken(kweights)
    kwins = 0
    while len(n) > 0:
        # Can n cheat and win?
        if n[-1] > k.weights[0]:
            index = next( i for i, w in enumerate(n) if w > k.weights[0] )
            k_play = k.play(k.weights[-1] + 1)
            if k_play > n[index]:
                raise Exception("Shouldn't happen")
            del n[index]
        else:
            n_play = n.pop()
            k_play = k.play(n_play)
            if k_play < n_play:
                raise Exception("Really shouldn't happen")
            else:
                kwins += 1
    return kwins


num_cases = int(input())
for case in range(1, num_cases+1):
    num_blocks = int(input())
    nblocks = [float(x) for x in input().split()]
    kblocks = [float(x) for x in input().split()]
    print("Case #{}: {} {}".format(case, num_blocks - DWar(kblocks, nblocks), 
        num_blocks - War(kblocks, nblocks)))
