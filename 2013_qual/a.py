def WinRow(row, winning_chars):
    return all(c in winning_chars for c in row)

def GridWin(grid, winning_chars):
    if any(WinRow(row, winning_chars) for row in grid):
        return True
    for column in range(4):
        if WinRow( (r[column] for r in grid), winning_chars ):
            return True
    if WinRow( (grid[c][c] for c in range(4)), winning_chars ):
        return True
    if WinRow( (grid[c][3-c] for c in range(4)), winning_chars ):
        return True
    return False
   
def Xwin(grid):
    return GridWin(grid, "XT")

def Owin(grid):
    return GridWin(grid, "OT")

num_cases = int(input())
for case in range(1, num_cases+1):
    grid = [input() for _ in range(4)]
    input()
    if Xwin(grid):
        output = "X won"
    elif Owin(grid):
        output = "O won"
    elif any( any(c == "." for c in row) for row in grid ):
        output = "Game has not completed"
    else:
        output = "Draw"
    print("Case #{}: {}".format(case, output))
