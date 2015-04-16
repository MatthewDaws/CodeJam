num_cases = int(input())
for case in range(1, num_cases+1):

    s = input()
    #s = "6 2 0 2 1 1 2 11"
    n, A, B, C, D, x0, y0, M = [int(x) for x in s.split()]
   
    trees = []
   
    X = x0
    Y = y0
    trees.append( (X,Y) )
    for i in range(1,n):
        X = (A * X + B) % M
        Y = (C * Y + D) % M
        trees.append( (X,Y) )
      
    mods = dict()
    modlens = dict()
    for xm in range(3):
        for ym in range(3):
            mods[ (xm,ym) ] = [(x,y) for (x,y) in trees if x % 3 == xm and y % 3 == ym]
            modlens[ (xm,ym) ] = len(mods[ (xm,ym) ])

    choices = 0
    for xm in range(3):
        for ym in range(3):
            choices += modlens[(xm,ym)] * (modlens[(xm,ym)] - 1) * (modlens[(xm,ym)] - 2) // 6

    choices += modlens[(0,0)] * modlens[(1,0)] * modlens[(2,0)]
    choices += modlens[(0,1)] * modlens[(1,1)] * modlens[(2,1)]
    choices += modlens[(0,2)] * modlens[(1,2)] * modlens[(2,2)]

    choices += modlens[(0,0)] * modlens[(0,1)] * modlens[(0,2)]
    choices += modlens[(1,0)] * modlens[(1,1)] * modlens[(1,2)]
    choices += modlens[(2,0)] * modlens[(2,1)] * modlens[(2,2)]

    choices += modlens[(0,0)] * modlens[(1,1)] * modlens[(2,2)]
    choices += modlens[(0,0)] * modlens[(1,2)] * modlens[(2,1)]
    choices += modlens[(0,1)] * modlens[(1,0)] * modlens[(2,2)]
    choices += modlens[(0,1)] * modlens[(1,2)] * modlens[(2,0)]
    choices += modlens[(0,2)] * modlens[(1,0)] * modlens[(2,1)]
    choices += modlens[(0,2)] * modlens[(1,1)] * modlens[(2,0)]

    print("Case #{}: {}".format(case, choices))
