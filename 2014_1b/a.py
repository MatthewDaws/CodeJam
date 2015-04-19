def min_diff(nums):
    """nums = list of integers.
    returns min( sum( abs(t-n) for t in nums ) for n an integer)"""
    if len(nums) == 0:
        return 0
    x = list(nums)
    x.sort()
    n = x[ len(x) // 2 ]
    return sum( abs(t-n) for t in x)

def repeat_list(input):
    """in = string like "aaaabbbcd"
    output list of tuples: (char, repeat) so in example, [ ("a",4), ("b", 3), ("c",1), ("d",1) ]"""
    out = []
    index = 0
    while index < len(input):
        current_char = input[index]
        length = 0
        while index < len(input) and input[index] == current_char:
            index += 1
            length += 1
        out.append( (current_char, length) )
    return out

num_cases = int(input())
for case in range(1, num_cases+1):
    num_lines = int(input())
    lines = [input() for _ in range(num_lines)]
    data = [repeat_list(s) for s in lines]
    letters = [ [c for (c,l) in line] for line in data]
    consistent = True
    for index in range(1, len(letters)):
        if letters[0] != letters[index]:
            consistent = False
            break
    if not consistent:
        output = "Fegla Won"
    else:
        lengths = [[l for (c,l) in line] for line in data]
        #print(lengths)
        #print(list(zip(*lengths)))
        output = sum( min_diff( line ) for line in zip(*lengths))

    print("Case #{}: {}".format(case, output))

        