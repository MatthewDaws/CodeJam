class Route:
    def __init__(self, neighbours, num_cities):
        self.neighbours = neighbours
        self.num_cities = num_cities
        self.visited = set() # Cities we've visited
        self.returns = [] # Cities we current have a "return ticket" to
        self.current = None

    def clone(self):
        r = Route(self.neighbours, self.num_cities)
        r.visited = set(self.visited)
        r.returns = self.returns[:]
        r.current = self.current
        return r

    def move(self, city):
        """Go to `city`, so set as start point.  Takes a "greedy" approach to route finding."""
        if len(self.visited) == 0:
            # Set first city!
            self.visited.add(city)
            self.current = city
            return
        if city not in self.neighbours[self.current]:
            # So need to use some return tickets
            index = len(self.returns) - 1
            while index >= 0 and city not in self.neighbours[ self.returns[index] ]:
                index -= 1
            if index == -1: # No path found
                raise Exception("Cannot travel to that city from current city")
            self.current = self.returns[index]
            self.returns = self.returns[:index]
        self.returns.append(self.current)
        self.visited.add(city)
        self.current = city

    def can_goto(self):
        """Return a list of all cities can visit.
        Actually returns a generator, and in the order our greedy algorithm needs
        (i.e. least use of return tickets first"""
        if len(self.visited) == 0:
            return
        yield from self.neighbours[self.current]
        for parent in reversed(self.returns):
            yield from self.neighbours[parent]

    def still_connected(self):
        """If we remove cities we have visited and do not have return tickets to,
        is the graph still connected?"""
        cannot_goto = [city for city in self.visited if city not in self.returns]
        cannot_goto.remove(self.current)
        # DFS to try to walk all of graph to test connectivity
        tovisit = [self.current]
        visited = set(cannot_goto)
        while len(tovisit) > 0:
            city = tovisit.pop()
            visited.add(city)
            tovisit.extend( c for c in self.neighbours[city] if c not in visited)
        return len(visited) == self.num_cities

    def cities_remaining(self):
        return self.num_cities - len(self.visited)
                    
num_cases = int(input())
for case in range(1, num_cases+1):
    num_cities, num_flights = [int(x) for x in input().split()]
    zips = { city : int(input()) for city in range(1, num_cities+1) }
    edges = [ [int(x) for x in input().split()] for _ in range(num_flights) ]
    # Move to dictionary form.  Nodes should be 1 .. num_cities
    neighbours = { city: [] for city in range(1, num_cities+1) }
    for edge in edges:
        neighbours[ edge[0] ].append( edge[1] )
        neighbours[ edge[1] ].append( edge[0] )

    output = ""
    visited = []
    route = Route(neighbours, num_cities)
    revzips = [ (zips[c], c) for c in zips ]
    revzips.sort( key = lambda pair : pair[0] )
    # Can start at any city; so start at lowest ZIP code
    route.move(revzips[0][1])
    output += str(revzips[0][0])
    del revzips[0]

    while route.cities_remaining() > 0:
        canvisit = list(route.can_goto())
        for index, (zip, city) in enumerate(revzips):
            if city in canvisit:
                r = route.clone()
                r.move(city)
                if r.still_connected():
                    route.move(city)
                    output += str(zip)
                    del revzips[index]
                    break

    print("Case #{}: {}".format(case, output))
