# -*- coding: utf-8 -*-

with open("garbled_email_dictionary.txt") as f:
    words = [line.rstrip() for line in f]
if len(words) != 521196:
    raise Exception("Didn't read correct number")

for i in range(len(words) - 2):
    if not ( words[i] < words[i+1] ):
        raise Exception("Not sorted!")

for word in words:
    if len(word) > 10:
        raise Exception("Assumed all words were at most 10 letters!")

wordsset = set(words)

# Generate words with one error
for word in words:
    for e1 in range(len(word)):
        wordsset.add( word[:e1] + "_" + word[e1+1:] )

# Generate words with two errors
for word in words:
    for e1 in range(len(word)):
        for e2 in range(e1+5, len(word)):
            S = word[:e1] + "_" + word[e1+1:]
            wordsset.add(S[:e2] + "_" + S[e2+1:])


# Helper function
def add_errors_in(nextn, last_error_table, postfix_length, errors, n):
    # postfix_length = length of word we can add from the dictionary
    # errors = list of errors indexed into postfix
    errortable = last_error_table[n - postfix_length]
    for e in errortable:
        if errortable[e] == -1:
            continue
        # See if we can use this error count
        if len(errors) == 0 or min(errors) >= errortable[e]:
            if len(errors) == 0:
                this_last_error = max(0, errortable[e] - postfix_length)
            else:
                this_last_error = max(0, 5 - ( postfix_length - max(errors) ))
            if e + len(errors) not in nextn:
                nextn[e + len(errors)] = this_last_error
            else:
                nextn[e + len(errors)] = min(this_last_error, nextn[e + len(errors)])

num_cases = int(input())
for case in range(1, num_cases+1):
    S = input()

    # Build DP table
    # (n,e) --> least k so we can deal with first n>=0 letters of S with e>=0 errors
    #           with the next k letters needing to be correct (so 0 <= k <= 4)
    # If (n,e) is not possible, then return -1
    # For efficiency, (n,e) is actually last_error_table[n][e]
    last_error_table = dict()
    last_error_table[0] = { 0 : 0 }
    for n in range(1, len(S)+1):
        # Try to find for n+1 given previous results
        nextn = dict()
        # Try with no further errors
        for length in range(1, min(11, n + 1)):
            postfix = S[n-length:n]
            if postfix in wordsset:
                add_errors_in(nextn, last_error_table, length, [], n)
        # Try with one error
        for length in range(1, min(11, n + 1)):
            for e1 in range(0,length):
                postfix = S[n-length:n]
                postfix = postfix[:e1] + "_" + postfix[e1+1:]
                if postfix in wordsset:
                    add_errors_in(nextn, last_error_table, length, [e1], n)
        # Try with two errors
        for length in range(1, min(11, n + 1)):
            for e1 in range(0, length):
                for e2 in range(e1 + 5, length):
                    postfix = S[n-length:n]
                    postfix = postfix[:e1] + "_" + postfix[e1+1:]
                    postfix = postfix[:e2] + "_" + postfix[e2+1:]
                    if postfix in wordsset:
                        add_errors_in(nextn, last_error_table, length, [e1, e2], n)
        # Add in -1 to show lengths we can't do
        if len(nextn) == 0:
            nextn[0] = -1
        maxerror = max(nextn)
        for e in range(0, maxerror+1):
            if e not in nextn:
                nextn[e] = -1
        last_error_table[n] = nextn

    # Answer is then the least e so that last_error_table[len(S)][e] != -1
    errordict = last_error_table[len(S)]
    maxerror = max(errordict)
    output = "PROBLEM"
    for e in range(0, maxerror+1):
        if errordict[e] != -1:
            output = e
            break

    print("Case #{}: {}".format(case, output))
