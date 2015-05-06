import itertools

def reshape(it, R, C):
    out = []
    for rows in range(R):
        out.append( [next(it) for _ in range(C)] )
    return out

def nbhs(row, col, R, C):
    out = []
    if row != 0:
        out.append( (row-1, col))
    if row != R - 1:
        out.append( (row+1, col))
    if col != 0:
        out.append( (row, col-1))
    if col != C - 1:
        out.append( (row, col+1))
    return out

def unhappy(matrix):
    num_rows = len(matrix)
    num_cols = len(matrix[0])
    count = 0
    for row in range(num_rows):
        for col in range(num_cols):
            if matrix[row][col] == 1:
                count += sum( matrix[n[0]][n[1]] == 1 for n in nbhs(row, col, num_rows, num_cols) )
    return count

def solve(R, C, N):
    best = -1
    for arr in itertools.product([0,1], repeat = R*C):
        if sum(arr) == N:
            arrangement = reshape(iter(arr), R, C)
            count = unhappy(arrangement)
            if best == -1 or count < best:
                best = count
    return best // 2


num_cases = int(input())
for case in range(1, num_cases+1):
    R, C, N = [int(x) for x in input().split()]
    output = solve(R, C, N)
    print("Case #{}: {}".format(case, output))
