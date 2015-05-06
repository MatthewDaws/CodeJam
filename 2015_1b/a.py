def flip(num):
    """Returns -1 if cannot flip (ends in 0 in decimal) or otherwise flipped."""
    if num <= 0 or ( num % 10 ) == 0:
        return -1
    return int("".join(reversed("{}".format(num))))

def solve_fast(num):
    if num <= 10:
        return num
    count = 0
    # Decrease to ???0001
    if num % 10 == 0:
        return 1 + solve_fast(num - 1)
    if num % 10 > 0:
        digits = "{}".format(num)
        number_digits = len( digits )
        last_half = int( digits[number_digits//2 : ] )
        newnum = digits[ : number_digits//2] + "0" * ((number_digits - 1) // 2) + "1"
        newnum = int( newnum )
        if newnum < num:
            count = last_half - 1
            #print("Moved to", num)
            num = newnum
    # Try flipping
    newnumflipped = flip(num)
    if newnumflipped != -1 and newnumflipped < num:
        count += 1
        num = newnumflipped
        #print("Flipped to", num)
    # Now decrease to 10^k
    pow10 = 1
    while pow10 <= num:
        pow10 *= 10
    pow10 = pow10 // 10
    count += ( num - pow10 )
    return 1 + count + solve_fast(pow10 - 1)

num_cases = int(input())
for case in range(1, num_cases+1):
    N = int(input())
    output = solve_fast(N)
    print("Case #{}: {}".format(case, output))
