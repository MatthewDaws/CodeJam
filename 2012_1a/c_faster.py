from collections import namedtuple
Car = namedtuple("Car", ["speed","pos"])

from collections import defaultdict
from fractions import Fraction

def fraction_diff_less5(a, b):
    # return abs(a-b) < 5
    # -5 * a.d * b.d < a.n*b.d - b.n*a.d < 5 * a.d * b.d
    x = abs(a.numerator * b.denominator - b.numerator * a.denominator)
    y = 5 * a.denominator * b.denominator
    return x < y

def fraction_equal_5(a, b):
    # return a == b - 5
    # a.n * b.d == b.n * a.d - 5 * a.d * b.d
    x = a.numerator * b.denominator
    y = ( b.numerator - 5 * b.denominator) * a.denominator
    return x == y

class SideAssignment:
    def __init__(self, cars, time):
        self.cars = [ Car(car.speed, car.pos + car.speed * time) for car in cars ]
        self.build_graph()
        #print("Time=", time, "-->")
        #self.printcars()
        #print("Fixed:", self.fixed)
        #print("Others:", self.others)
        #print("Graph:", self.neighbours)

    def printcars(self):
        cars = [ (i,car) for i, car in enumerate(self.cars) ]
        cars.sort(key = lambda pair : pair[1].pos)
        for car in cars:
            print("{}) {} -- {}".format(car[0],str(car[1].pos), car[1].speed))

    def graph_add_edge(self, i, j):
        self.neighbours[i].add(j)
        self.neighbours[j].add(i)

    def build_graph(self):
        # Split cars into categories:
        #    - Those which are about to overtake or be overtaken
        #    - Those which overlap (so have fixed position)
        #    - Others, which wlog can be on the left
        # The graph will build links car (i,j) if i and j overlap, or will because
        # of overtaking.
        self.neighbours = defaultdict(set)
        self.fixed = set()
        for i, car in enumerate(self.cars):
            for j, c in enumerate(self.cars):
                #if j != i and abs(car.pos - c.pos) < 5:
                if j != i and fraction_diff_less5(car.pos, c.pos):
                    self.fixed.add(i)
                    self.graph_add_edge(i, j)
                #if car.speed > c.speed and car.pos == c.pos - 5:
                if car.speed > c.speed and fraction_equal_5(car.pos, c.pos):
                    self.graph_add_edge(i, j)
        self.others = [ i for i, _ in enumerate(self.cars) if i not in self.neighbours ]
        self.unassigned = { i for i in self.neighbours if i not in self.fixed }

    def possible_extensions_old(self, current_road_side):
        initial = { i : "L" for i in self.others }
        for i in self.fixed:
            initial[i] = current_road_side[i]
        # Check this is consistent
        for index in initial:
            for i in self.neighbours[index]:
                if i in initial and initial[index] == initial[i]:
                    return []
        # Assign other choices
        choices = [ initial ]
        for index in self.unassigned:
            new_choices = []
            for choice in choices:
                # Try to assign index
                sides = set( choice[i] for i in self.neighbours[index] if i in choice )
                sides = {"L", "R"}.difference(sides)
                for side in sides:
                    nc = dict(choice)
                    nc[index] = side
                    new_choices.append(nc)
            choices = new_choices
            if len(choices) == 0:
                return []
        # Convert to list to return
        ret_list = []
        for choice in choices:
            ret_list.append( tuple( choice[i] for i in range(len(self.cars)) ) )
        return ret_list

    def possible_extensions(self, current_road_side):
        initial = [ "?" for _ in range(len(self.cars)) ]
        for i in self.others:
            initial[i] = "L"
        for i in self.fixed:
            initial[i] = current_road_side[i]
        # Check this is consistent
        for index in range(len(self.cars)):
            if initial[index] != "?":
                for i in self.neighbours[index]:
                    if initial[index] == initial[i]:
                        return []
        # Assign other choices
        choices = [ initial ]
        for index in self.unassigned:
            new_choices = []
            for choice in choices:
                # Try to assign index
                sides = set( choice[i] for i in self.neighbours[index] if choice[i] != "?" )
                sides = {"L", "R"}.difference(sides)
                for side in sides:
                    nc = choice[:]
                    nc[index] = side
                    new_choices.append(nc)
            choices = new_choices
            if len(choices) == 0:
                return []
        return choices

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
        sideassign = SideAssignment(cars, time)
        new_assignments = set()
        for assignment in side_road_assignments:
            for choice in sideassign.possible_extensions(assignment):
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