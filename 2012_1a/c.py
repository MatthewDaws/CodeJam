from collections import namedtuple
Car = namedtuple("Car", ["speed","pos"])

from collections import defaultdict
from fractions import Fraction

class InvalidAssignment(Exception):
    pass

def check_assignments(edges, assignment, index):
    """Check if `assignment[index]` can be set consistently.
    Returns a list of new indices which are added to assignment.
    Throws InvalidAssignment if problem."""
    otherside = { "L":"R", "R":"L" }
    if index not in edges:
        return []
    changed = []
    for nhb in edges[index]:
        if nhb in assignment:
            if assignment[nhb] != otherside[ assignment[index] ]:
                raise InvalidAssignment()
        else:
            assignment[nhb] = otherside[ assignment[index] ]
            changed.append(nhb)
    return changed

def add_index_to_assignments(edges, assignment, index, what):
    """Tries `assignment[index] = what` and changes all other assignments.
    Returns new valid assignment, or empty dictionary."""
    na = dict(assignment)
    na[index] = what
    todo = [ index ]
    while len(todo) > 0:
        index = todo.pop()
        try:
            todo.extend( check_assignments(edges, na, index) )
        except InvalidAssignment:
            return dict()
    return na

def all_assignments(side_road, cars):
    """Returns list of possible assignments which allow overtaking to occur.
       side_road = current side of the road cars are on."""
    # The only cars we need to worry about are those which are just about to be
    # overtaken, or just about to overtake.
    # All other cars can continue in their current lane: either they can't move
    # anyway, or they are free to move but their movements will have no effect on
    # any other car.
    # Get a graph algorithm: an edge joins cars if they are "interacting".
    # We initially assign "L" or "R" as in `side_road` to those cars which have
    # no neighbours, or those cars which overlap (an invariant of our previous
    # assignments is that these will be consistent).
    # Then those which are "bumper to bumper" must be assigned in a coherent way.
    # E.g. this:  L -- ? -- R is impossible
    # This  L -- ? -- L means ? must be R
    # Algorithm: all those nodes which are assigned are in a "todo list".  Then
    # We walk the "todo list" and assign to any neighbours the opposite, or if the
    # neighbour is already assigned, check consistency.
    # If ever get a component of just "?" then we have a choice, and we should return
    # all choices.

    # Those we must copy from `side_road`
    initial = dict()
    for index, car in enumerate(cars):
        interacting = [ j for j, c in enumerate(cars) if abs( car.pos - c.pos ) < 5 ]
        if len(interacting) > 1:
            initial[index] = side_road[index]

    # Those we must choose
    edges = defaultdict(set)
    for index, car in enumerate(cars):
        will_overtake = [ j for j, c in enumerate(cars) if
                ( car.pos == c.pos - 5 and car.speed > c.speed ) ]
        for j in will_overtake:
            edges[index].add(j)
            edges[j].add(index)

    # Add in those which have no interaction
    for index, car in enumerate(cars):
        if index not in initial and index not in edges:
            #initial[index] = side_road[index]
            initial[index] = "L"

    #print("Initial choices:", initial)
    #print("Edges:", edges)

    # Find those choices which are forced and check consistency
    todo = list(initial)
    while len(todo) > 0:
        index = todo.pop()
        try:
            todo.extend( check_assignments(edges, initial, index) )
        except InvalidAssignment:
            return []

    # Have assigned all we can.  Maybe there are other components of
    # undecided.  Idea is to pick an undecided point, set it to "L", and then
    # run the above algorithm again.

    #print("Initial choices:", initial)
    choices = [ initial ]
    while len( choices[0] ) < len(cars):
        index = next( i for i, _ in enumerate(cars) if i not in choices[0] )
        new_choices = []
        for choice in choices:
            nc = add_index_to_assignments(edges, choice, index, "L")
            if len(nc) > 0:
                new_choices.append(nc)
            nc = add_index_to_assignments(edges, choice, index, "R")
            if len(nc) > 0:
                new_choices.append(nc)
        choices = new_choices
        if len(choices) == 0:
            return []

    # Convert to list of tuples and return
    return_list = []
    for choice in choices:
        return_list.append( tuple( choice[i] for i in range(len(cars)) ) )
    return return_list

def solve(initial_side_road, cars):
    # Possible event times, when faster car bumper touches rear of slower car
    event_times = []
    for i, fast in enumerate(cars):
        for slow in cars[:i]:
            if fast.speed == slow.speed:
                break
            # Solve t >=0 and fast.pos + fast.speed * t == slow.pos + slow.speed * t - 5
            t = Fraction(slow.pos - fast.pos - 5, fast.speed - slow.speed)
            #t = (slow.pos - fast.pos - 5) / (fast.speed - slow.speed)
            if t >= 0:
                event_times.append(t)
    event_times.sort()
    # Run simulation
    side_road_assignments = [ initial_side_road[:] ]
    for time in event_times:
        current_cars = [ Car(car.speed, car.pos + car.speed * time) for car in cars ]
        #print("Event point:", time, current_cars)
        print("Event point:", time, "choices:", len(side_road_assignments))
        new_assignments = set()
        for assignment in side_road_assignments:
            for choice in all_assignments(assignment, current_cars):
                new_assignments.add( tuple(choice) )
        side_road_assignments = new_assignments
        if len(side_road_assignments) == 0:
            return float(time)
    return "Possible"


num_cases = int(input())
for case in range(1, num_cases + 1):
    num_cars = int(input())
    data = []
    for _ in range(num_cars):
        line = input().split()
        data.append( (int(line[1]), int(line[2]), line[0]) )
    data.sort()
    side_road = [ line[2] for line in data ]
    cars = [ Car(line[0], line[1]) for line in data ]
    #print("Setup:", cars)
    #print(side_road)

    output = solve(side_road, cars)

    print("Case #{}: {}".format(case, output))