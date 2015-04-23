# -*- coding: utf-8 -*-

def situation_at_time(T, M):
    """Returns dictionary, barbers[barber] = (Customers served, time until next free)
    If `time until next free` == 0 then read now; otherwise _one further customer_
    will have been served at the end."""
    barbers = dict()
    for barber, rate in enumerate(M):
        cs = (T + rate - 1) // rate
        tunf = rate - (T % rate)
        if tunf == rate:
            tunf = 0
        barbers[barber+1] = (cs, tunf)
    return barbers

def customers_served_in_time(T, M):
    barbers = situation_at_time(T, M)
    return sum( barbers[barber][0] for barber in range(1, len(M)+1) )

def binary_search(M, place):
    high = 2
    while customers_served_in_time(high, M) < place:
        high += high
    low = high // 2
    if customers_served_in_time(low, M) >= place:
        low = 0
    # Invariant is customers_served_in_time(low, M) < place and
    # customers_served_in_time(high, M) >= place
    while high - low > 1:
        mid = (high + low) // 2
        if customers_served_in_time(mid, M) < place:
            low = mid
        else:
            high = mid
    return low

def step_forward_slow(M, barbers, place):
    """`barbers` should be list of the barbers of time until next free
    `place` your current place in the queue; 1 == next place
    returns the number of the barber who cuts your hair, from 1."""
    num_barbers = len(M)
    state = barbers[:]
    while True:
        # Find next free
        time = min(state)
        state = [x - time for x in state]
        indices = [index for index, t in enumerate(state) if t == 0]
        for index in indices:
            place -= 1
            if place == 0:
                return index + 1
            state[index] = M[index]

num_cases = int(input())

for case in range(1, num_cases+1):
    num_barbers, your_place = [int(x) for x in input().split()]
    M = [int(x) for x in input().split()]
    
    time = binary_search(M, your_place)
    #print("Search time begins at", time)
    barbers = situation_at_time(time, M)
    num_served = sum( barbers[barber][0] for barber in barbers )
    state = [ barbers[barber][1] for barber in barbers ]
    #print("barbers --> ", barbers)
    #print("Already served:", num_served)
    #print("State is:", state)
    output = step_forward_slow(M, state, your_place - num_served)

    if your_place <= 10000:
        output1 = step_forward_slow(M, [0]*num_barbers, your_place)
        if output != output1:
            raise Exception("FUCK")

    print("Case #{}: {}".format(case, output))