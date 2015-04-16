num_cases = int( input() )
for case in range(1, num_cases+1):
    #print("CASE: ", case)
    num_flavours = int( input() )
    num_customers = int( input() )
    customers = []
    for _ in range(num_customers):
        prefs = input().split()
        prefs = [int(x) for x in prefs[1:]]
        customers.append( prefs )
        #print(prefs)
    is_malted = [0] * num_flavours
    # Find picky customers
    for prefs in customers:
        if len(prefs) == 2 and prefs[1] == 1:
            flavour = prefs[0] - 1
            is_malted[flavour] = 1
    #print("--->", is_malted)
    # Satisfied all now?
    impossible = False
    pref_index = 0
    while pref_index < len(customers):
        prefs = customers[pref_index]
        index = 0
        happy = False
        maltedpref = 0
        while index + index < len(prefs):
            flavour = prefs[index+index]
            malted = prefs[index+index+1]
            if malted == 1:
                maltedpref = flavour
            if is_malted[flavour-1] == malted:
                happy = True
                break
            index += 1
        if not happy:
            # Could be that making something malted helps?
            if maltedpref > 0:
                is_malted[maltedpref-1] = 1
                pref_index = 0
                #print("Forced to additionally make flavour", maltedpref,"malted!")
            else:
               impossible = True
               #print("Can't satisfy this customer:", prefs)
               break
        else:
           pref_index += 1 # Next check
    if impossible:
        print("Case #{}: IMPOSSIBLE".format(case))
    else:
        print("Case #{}: {}".format(case, " ".join(str(x) for x in is_malted)) )
