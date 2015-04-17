num_cases = int( input() )
for case in range(num_cases):
    num_search_engines = int( input() )
    search_engines = [input() for _ in range(num_search_engines)]
    num_queries = int( input() )
    queries = []
    for _ in range(num_queries):
        name = input()
        index = search_engines.index(name)
        queries.append( index )

    index = 0
    swaps = 0
    while True:
        used = set()
        while len(used) < num_search_engines and index < num_queries:
            used.add( queries[index] )
            index += 1
        if len(used) == num_search_engines:
            swaps += 1
        if index == num_queries:
            break
        # So last added index broke, so reduce to add again
        index -= 1
    print("Case #{}: {}".format(case+1, swaps))
