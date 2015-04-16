def solve_normal(rows, columns, mines):
    """Solve assuming columns >= rows and rows > 2
    Returns (is_impossible, output)"""
    excess = mines - min(mines, rows * columns - 9)
    if excess > 0:
        if excess not in [1, 3, 5, 8]:
            return True, []
    mines = mines - excess
    widths = dict()
    current_row = rows
    while mines > 0 and current_row > 2:
        if mines <= columns - 2:
            widths[current_row] = mines
            mines = 0
        elif mines == columns - 1:
            widths[current_row] = columns - 2
            mines = 1
        else:
            widths[current_row] = columns
            mines -= columns
        current_row -= 1
    if current_row == 2 and mines > 0:
        if mines % 2 == 1:
            overshot = True
            mines += 1
        else:
            overshot = False
        widths[2] = mines // 2
        if overshot:
            if widths[3] == columns:
                widths[3] = columns - 3
                widths[2] += 1
            else:
                widths[3] -= 1
    # Insert extra data to get all widths
    for row in range(2, rows+1):
        if row not in widths:
            widths[row] = 0
    # Make map
    output = []
    row2 = "." * (columns - widths[2]) + "*" * widths[2]
    output.append(row2)
    output.append(row2)
    for row in range(3, rows+1):
        output.append( "." * (columns - widths[row]) + "*" * widths[row] )
    # Deal with excess
    if excess > 0:
        if excess == 1:
            output[2] = output[2][:2] + "*" + output[2][3:]
        elif excess >= 3:
            output[2] = "***" + output[2][3:]
            if excess == 5:
                output[0] = output[0][:2] + "*" + output[0][3:]
                output[1] = output[1][:2] + "*" + output[1][3:]
            elif excess == 8:
                output[0] = ".**" + output[0][3:]
                output[1] = "***" + output[1][3:]            
    return False, output

num_cases = int(input())

for case in range(1,num_cases+1):
    # rows == height,  columns == width
    rows, columns, mines = [int(x) for x in input().split()]
    if rows < columns:
        reversed = True
        rows, columns = columns, rows
    else:
        reversed = False
    # So now "tall and thin" width <= height
    if columns == 1:
        if mines >= rows:
            is_impossible = True
        else:
            is_impossible = False
            output = ["." for _ in range(rows - mines)]
            output.extend( ["*" for _ in range(mines)] )
    elif columns == 2:
        if mines <= 2*rows - 4 and mines % 2 == 0:
            is_impossible = False
            output = [".." for _ in range(rows - mines//2)]
            output.extend("**" for _ in range(mines//2))
        elif mines == 2*rows - 1:
            is_impossible = False
            output = [".*"]
            output.extend("**" for _ in range(rows-1))
        else:
            is_impossible = True
    else:
        is_impossible, output = solve_normal(rows, columns, mines)
    print("Case #{}:".format(case))
    if is_impossible:
        print("Impossible")
    else:        
        if reversed:
            output = [ "".join(row[col] for row in output) for col in range(columns) ]
        output[0] = "c" + output[0][1:]
        for row in output:
            print(row)
