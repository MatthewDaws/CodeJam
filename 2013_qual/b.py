num_cases = int(input())
for case in range(1, num_cases+1):
    rows, cols = [int(x) for x in input().split()]
    grid = [ [int(x) for x in input().split()] for _ in range(rows) ]
    # Constraint is that each entry must be equal to the maximum of the
    # row _or_ column it is in
    row_maxs = [ max( row ) for row in grid ]
    col_maxs = [ max( row[c] for row in grid) for c in range(cols) ]
    cando = True
    for row in range(rows):
        for col in range(cols):
            entry = grid[row][col]
            if entry != row_maxs[row] and entry != col_maxs[col]:
                cando = False
                break
        if not cando:
            break
    output = "YES" if cando else "NO"
    print("Case #{}: {}".format(case, output))
