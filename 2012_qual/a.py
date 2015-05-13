letter_map = {"a": "y", "o": "e", "z": "q"}

def add_to_map(input, output):
    if len(input) != len(output):
        raise Exception("Lengths differ!")
    for i, o in zip(input, output):
        if i in letter_map:
            if letter_map[i] != o:
                raise Exception("We thought {} -> {} already!".format(i,o))
        else:
            letter_map[i] = o

add_to_map("our language is impossible to understand",
            "ejp mysljylc kd kxveddknmc re jsicpdrysi")
add_to_map("there are twenty six factorial possibilities",
            "rbcpc ypc rtcsra dkh wyfrepkym veddknkmkrkcd")
add_to_map("so it is okay if you want to just give up",
            "de kr kd eoya kw aej tysr re ujdr lkgc jv")

unknowns = [ c for c in "abcdefghijklmnopqrstuvwxyz" if c not in letter_map ]
if len(unknowns) > 1:
    raise Exception("More than one unknown!")

inv = dict()
for c in letter_map:
    inv[ letter_map[c] ] = c

unknowns_inv = [ c for c in "abcdefghijklmnopqrstuvwxyz" if c not in inv ]
if len(unknowns_inv) > 1:
    raise Exception("More than one missing!")

inv[ unknowns_inv[0] ] = unknowns[0]

num_cases = int(input())
for case in range(1, num_cases+1):
    encoded = input()
    decoded = [ inv[c] for c in encoded ]
    print("Case #{}: {}".format(case, "".join(decoded)))
