# -*- coding: utf-8 -*-

with open("garbled_email_dictionary.txt") as f:
    words = [line.rstrip() for line in f]
if len(words) != 521196:
    raise Exception("Didn't read correct number")

for i in range(len(words) - 2):
    if not ( words[i] < words[i+1] ):
        raise Exception("Not sorted!")

wordsset = set(words)
reversed_words = ["".join(reversed(word)) for word in words]
reversed_words.sort()
reversed_wordsset = set(reversed_words)

def locate_in_reversed_words(prefix):
    """Return index of first words in `words` starting with prefix, or -1 if none"""
    if reversed_words[0].startswith(prefix):
        return 0
    low = 0
    high = len(reversed_words) - 1
    if not ( reversed_words[low] < prefix and prefix <= reversed_words[high] ):
        return -1
    while high - low > 1:
        mid = (high + low) // 2
        if reversed_words[mid] < prefix:
            low = mid
        else:
            high = mid
    if low == len(reversed_words) - 1 or not reversed_words[low+1].startswith(prefix):
        return -1
    return low + 1

def locate_in_words(prefix):
    """Return index of first words in `words` starting with prefix, or -1 if none"""
    if words[0].startswith(prefix):
        return 0
    low = 0
    high = len(words) - 1
    if not ( words[low] < prefix and prefix <= words[high] ):
        return -1
    while high - low > 1:
        mid = (high + low) // 2
        if words[mid] < prefix:
            low = mid
        else:
            high = mid
    if low == len(words) - 1 or not words[low+1].startswith(prefix):
        return -1
    return low + 1

def is_in_words(word):
    return word in wordsset

def yield_matches0(S):
    """Returns words which match the front of S with 0 errors"""
    for length in range(1, len(S)+1):
        if is_in_words(S[:length]):
            yield S[:length]

def yield_lengths_matches0(S):
    """As above, but returns just the length of the match."""
    for length in range(1, len(S)+1):
        if is_in_words(S[:length]):
            yield length

alphabet = "abcdefghijklmnopqrstuvwxyz"

def word_exists(S, error_at):
    """Does S, with index error_at an error, exist in words?"""
    # Only 26 letters in alphabet, so this is probably quickest we can do with
    # a large dictionary
    for c in alphabet:
        if c != S[error_at]:
            T = S[:error_at] + c + S[error_at + 1:]
            if is_in_words(T):
                return True
    return False

def matches1_list(S, last_error_index):
    # Equivalent to:
    #return list(set(yield_lengths_matches1(S, last_error_index)))
    # However, notice that for each (length, new_last_error_index) pair, for
    # each fixed value of `length`, we only care about the smallest
    # `new_last_error_index`.
    ret = []
    for length in range(min(10, len(S)), 0, -1):
        for error_at in range(max(0,5 + last_error_index), length):
            if word_exists(S[:length], error_at):
                ret.append((length, error_at - length))
                break
    return ret

def matches2_list_find(string, last_error_index):
    #print("--->", string, last_error_index)
    length = len(string)
    for error_at1 in range(length-4, -1, -1):
        for c1 in alphabet:
            if c1 != string[error_at1]:
                S1 = string[:error_at1] + c1 + string[error_at1 + 1:]
                #print("   Trying", S1[:error_at1+5])
                if locate_in_reversed_words(S1[:error_at1+5]) != -1:
                    # error_at2 = length - 1 - k corresponds to index k in S
                    # so need k >= 5 + last_error_index
                    # so error_at2 <= length - 6 - last_error_index
                    for error_at2 in range(error_at1 + 5, min(length, length - 5 - last_error_index)):
                        for c2 in alphabet:
                            if c2 != S1[error_at2]:
                                if S1[:error_at2] + c2 + S1[error_at2 + 1:] in reversed_wordsset:
                                    # error_at1 == 0 corresponds to -1
                                    return -1 - error_at1
    return 0

def matches2_list(S, last_error_index):
    # Equivalent to:
    #return list(set(yield_lengths_matches2(S, last_error_index)))
    # But with similar optimisations to above
    ret = []
    # In reversed, errors can be at 0 through len(S) - 1 - (5 + last_error_index)
    #   = len(S) - 6 - last_error_index
    for length in range(min(10,len(S)), max(0, 10 + last_error_index), -1):
        string = S[:length]
        string = "".join(reversed(string))
        error = matches2_list_find(string, last_error_index)
        if error < 0:
            ret.append((length, error))
    return ret

from collections import namedtuple
State = namedtuple("State", ["string", "last_error_index", "error_count"])

def match(S):
    """Depth first search with pruning."""
    best = (len(S)+4)//5
    to_consider = [ State(S, -5, 0) ]
    while len(to_consider) > 0:
        state = to_consider.pop()
        #print(state)
        if len(state.string) == 0:
            best = min(best, state.error_count)
            if best == 0:
                break
            continue
        if state.error_count > best:
            continue
            
        if state.error_count + 2 < best:
            news = matches2_list(state.string, state.last_error_index)            
            for length, ei in news:
                to_consider.append(State(state.string[length:], ei, state.error_count + 2))
            
        if state.error_count + 1 < best:
            news = matches1_list(state.string, state.last_error_index)
            for length, ei in news:
                to_consider.append(State(state.string[length:], ei, state.error_count + 1))
        
        for length in yield_lengths_matches0(state.string):
            to_consider.append(State(state.string[length:], state.last_error_index - length, state.error_count))
            
    return best


num_cases = int(input())
for case in range(1, num_cases+1):
    S = input()
    output = match(S)
    print("Case #{}: {}".format(case, output))
