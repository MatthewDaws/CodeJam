from collections import namedtuple
Point = namedtuple("Point", ["row", "col"])
Vector = namedtuple("Vector", ["x", "y"])   
#from fractions import Fraction
import math

class myFraction:
    def __init__(self, num, dem):
        """Quick and dirty fraction class."""
        if dem < 0:
            dem = -dem
            num = -num
        if isinstance(num, Fraction):
            self.num, self.dem = num.num, num.dem
            if isinstance(dem, Fraction):
                self.dem *= dem.num
                self.num *= dem.dem
            else:
                self.dem *= dem
        else:
            self.num = num
            if isinstance(dem, Fraction):
                self.dem = dem.num
                self.num *= dem.dem
            else:
                self.dem = dem

    def __repr__(self):
        return "Fraction({},{})".format(self.num, self.dem)

    def __hash__(self):
        return hash((self.num, self.dem))

    def __eq__(self, other):
        if isinstance(other, Fraction):
            return self.num * other.dem == self.dem * other.num
        return self.num == self.dem * other

    def __add__(self, other):
        if isinstance(other, Fraction):
            return Fraction(self.num * other.dem + self.dem * other.num, self.dem * other.dem)
        return Fraction(self.num + self.dem * other, self.dem)

    def __radd__(self, other):
        return Fraction(self.num + self.dem * other, self.dem)

    def __sub__(self, other):
        if isinstance(other, Fraction):
            return Fraction(self.num * other.dem - self.dem * other.num, self.dem * other.dem)
        return Fraction(self.num - self.dem * other, self.dem)

    def __rsub__(self, other):
        # Assume other is an int; want other - self
        return Fraction(self.dem * other - self.num, self.dem)

    def __mul__(self, other):
        if isinstance(other, Fraction):
            return Fraction(self.num * other.num, self.dem * other.dem)
        return Fraction(self.num * other, self.dem)

    def __rmul__(self, other):
        return Fraction(self.num * other, self.dem)

    def __lt__(self, other):
        if isinstance(other, Fraction):
            return self.num * other.dem < other.num * self.dem
        return self.num < other * self.dem

    def __le__(self, other):
        if isinstance(other, Fraction):
            return self.num * other.dem <= other.num * self.dem
        return self.num <= other * self.dem

    def __gt__(self, other):
        if isinstance(other, Fraction):
            return self.num * other.dem > other.num * self.dem
        return self.num > other * self.dem

    def __ge__(self, other):
        if isinstance(other, Fraction):
            return self.num * other.dem >= other.num * self.dem
        return self.num >= other * self.dem

    def __neg__(self):
        return Fraction(-self.num, self.dem)
    
    def __float__(self):
        return self.num / self.dem

class HallMirrors:
    def __init__(self, maze):
        self.num_rows = len(maze)
        self.num_cols = len(maze[0])
        self.maze = [ row[:] for row in maze ]
        # Find the location "X"
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                if self.maze[row][col] == "X":
                    #self.maze[row][col] = "."
                    self.maze[row] = self.maze[row][:col] + "." + self.maze[row][col+1:]
                    #self.position = Point(row + Fraction(1,2), col + Fraction(1,2))
                    self.position = Point(row + 0.5, col + 0.5)
        # Various setup
        self.construct_lines()
        self.find_concave_corners()
        self.find_convex_corners()

    def get(self, row, col):
        # Coordinate system is that (row,col) is the top left corner of the square
        if row < 0 or col < 0 or row >= self.num_rows or col >= self.num_cols:
            return "#"
        return self.maze[row][col]

    def find_concave_corners(self):
        self.corners = []
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                x = self.get(row,col)+self.get(row,col+1)+self.get(row+1,col)+self.get(row+1,col+1)
                #   ##  ##  .#  #.
                #   .#  #.  ##  ##
                if x == "##.#" or x == "###." or x == ".###" or x == "#.##":
                    self.corners.append( Point(row+1,col+1) )

    def find_convex_corners(self):
        self.ann_corners = []
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                x = self.get(row,col)+self.get(row,col+1)+self.get(row+1,col)+self.get(row+1,col+1)
                #   #.  .#  ..  ..
                #   ..  ..  #.  .#
                if x == "#..." or x == ".#.." or x == "..#." or x == "...#":
                    self.ann_corners.append( Point(row+1,col+1) )
                    
    def construct_lines(self):
        """Internal: Make a list of lines which are the mirrors."""
        # Make a list of line segments.  All go from top -> bottom or left -> right
        # Third entry is normal vector (1,0), (-1,0), (0,1), (0,-1) used for coalesing below
        horzs = []
        verts = []
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                if self.get(row, col) == "#":
                    if self.get(row, col - 1) == ".":
                        verts.append( (Point(row,col), Point(row + 1, col), (0,-1)) )
                    if self.get(row, col + 1) == ".":
                        verts.append( (Point(row,col + 1), Point(row + 1, col + 1), (0,1)) )
                    if self.get(row - 1, col) == ".":
                        horzs.append( (Point(row,col), Point(row, col + 1), (-1,0)) )
                    if self.get(row + 1, col) == ".":
                        horzs.append( (Point(row + 1,col), Point(row + 1, col + 1), (1,0)) )
        # Now join together horizontal or vertical
        self.all_lines = []
        for col in range(self.num_cols):
            this_col = [ line for line in verts if line[0].col == col ]
            this_col.sort(key = lambda line : line[0].row)
            index = 0
            while index < len(this_col) - 1:
                if this_col[index][1].row == this_col[index+1][0].row and this_col[index][2] == this_col[index+1][2]:
                    this_col[index] = (this_col[index][0], this_col[index+1][1], this_col[index][2])
                    del this_col[index+1]
                else:
                    index += 1
            self.all_lines.extend( (a,b) for (a,b,c) in this_col )
        for row in range(self.num_rows):
            this_row = [ line for line in horzs if line[0].row == row ]
            this_row.sort(key = lambda line : line[0].col)
            index = 0
            while index < len(this_row) - 1:
                if this_row[index][1].col == this_row[index+1][0].col and this_row[index][2] == this_row[index+1][2]:
                    this_row[index] = (this_row[index][0], this_row[index+1][1], this_row[index][2])
                    del this_row[index+1]
                else:
                    index += 1
            self.all_lines.extend( (a,b) for (a,b,c) in this_row )
        
    def __repr__(self):
        s = "\n".join(self.maze)
        s += "\nPlayer: {}".format(self.position)
        s += "\nConcave corners: {}".format(self.corners)
        s += "\nConvex corners: {}".format(self.ann_corners)
        s += "\nLines: {}".format(self.all_lines)
        return s

class Light:
    def __init__(self, direction, hall_mirrors):
        """direction: Vector."""
        self.direction = direction
        self.hm = hall_mirrors
        self.position = hall_mirrors.position
        self.distance_travelled = 0

    @staticmethod
    def distance(one, two):
        x = one.row - two.row
        y = one.col - two.col
        return math.sqrt( float(x * x + y * y) )
        
    def hit_point(self, p):
        """Returns distance to `p` or -1 if can't hit."""
        # Use least squares minimisation with floats
        # self.position + t * self.direction closest to p
        # x = self.position.row - p.row + self.direction.row * t
        # y = self.position.col - p.col + self.direction.col * t
        # min x*x+y*y over t
        # = (a+b*t)*(a+b*t) + (c+d*t)*(c+d*t)
        # = a*a+c*c + 2*a*b*t + 2*c*d*t + b*b*t*t + d*d*t*t
        # = A*t*t + 2*B*t + C with A > 0
        # Min at t = -B/A and value is C - B*B/A
        a = float(self.position.row) - float(p.row)
        b = float(self.direction.row)
        c = float(self.position.col) - float(p.col)
        d = float(self.direction.col)
        A = b*b + d*d
        B = a*b + c*d
        C = a*a + c*c
        if B < 0 and abs(C - B*B / A) < 1e-6:
            return Light.distance(self.position, p)
        return -1

    def hit_point_old(self, p):
        """Returns distance to `p` or -1 if can't hit."""
        # Solve self.position + t * self.direction == p for t > 0
        if self.direction.row == 0:
            if p.row != self.position.row:
                return -1
            #tcol = Fraction(p.col - self.position.col, self.direction.col)
            #if tcol <= 0:
            x = p.col - self.position.col
            if ( self.direction.col > 0 and x <= 0 ) or ( self.direction.col < 0 and x >= 0 ):
                return -1
            return self.distance(self.position, p)
        #trow = Fraction(p.row - self.position.row, self.direction.row)
        #if trow <= 0:
        x = p.row - self.position.row
        if ( self.direction.row > 0 and x <= 0 ) or ( self.direction.row < 0 and x >= 0 ):
            return -1
        if self.direction.col == 0:
            if p.col != self.position.col:
                return -1
            return Light.distance(self.position, p)
        #tcol = Fraction(p.col - self.position.col, self.direction.col)
        #if trow != tcol:
        y = p.col - self.position.col
        if x * self.direction.col != y * self.direction.row:
            return -1
        return Light.distance(self.position, p)
        
    def find_corners(self):
        """Generates (position, distance) pairs of intersections with "concave" corners
        which reflect back directly"""
        for p in self.hm.corners:
            d = self.hit_point(p)
            if d != -1:
                yield (p,d)

    def find_ann_corners(self):
        """Generates (position, distance) pairs of intersections with "concex" corners
        which absorb the light ray"""
        for p in self.hm.ann_corners:
            d = self.hit_point(p)
            if d != -1:
                yield (p,d)
    
    @staticmethod
    def line_intersect(x,d,x0,x1):
        """x,d,x0,x1 vectors, solves x + t*d = s*x0 + (1-s)*x2 for scalars t,s.
        Returns pair (True,(t, s)) or (False,(?,?))"""
        # Matrix A=(a b \\ c d)
        a = x0.row - x1.row
        b = -d.row
        c = x0.col - x1.col
        d = -d.col
        det = a * d - b * c
        if det == 0:
            return (False, (0,0))
        s, t = (x.row - x1.row), (x.col - x1.col)
        s, t = d * s - b * t, -c * s + a * t
        return True, (t/det, s/det)
    
    def find_next_intersection(self):
        """Generates intersection of ray with all lines.  Returns triple
        (intersection_point, distance, new_direction) where `new_direction` is the reflected
        direction vector."""
        for line in hm.all_lines:
            hit, (t, s) = self.line_intersect(self.position, self.direction, line[0], line[1])
            if hit and t > 1e-6 and 1e-6 < s and s < 1 - 1e-6:
                p = Point(self.position.row + t * self.direction.row, self.position.col + t * self.direction.col)
                normal = Point(line[1].col - line[0].col, line[0].row - line[1].row)
                normal_norm_sq = normal.row * normal.row + normal.col * normal.col
                dotp = normal.row * self.direction.row + normal.col * self.direction.col
                #refl = Point(Fraction(- 2 * dotp * normal.row, normal_norm_sq),
                #             Fraction(- 2 * dotp * normal.col, normal_norm_sq) )
                #refl = Point(self.direction.row + refl.row, self.direction.col + refl.col)
                refl = Point((- 2 * dotp * normal.row) / normal_norm_sq,
                             (- 2 * dotp * normal.col) / normal_norm_sq )
                refl = Point(self.direction.row + refl.row, self.direction.col + refl.col)
                # Ensure all integer
                #refl = Point(self.direction.row * normal_norm_sq - 2 * dotp * normal.row,
                #            self.direction.col * normal_norm_sq - 2 * dotp * normal.col)
                yield (p, self.distance(self.position, p), refl)

    def can_hit_start(self):
        """Returns distance to the starting point, or -1 if can't hit."""
        return self.hit_point(self.hm.position)
        
    def at_start(self, refl):
        pass

    def hit_concave_corner(self, refl):
        self.direction = Point(-self.direction.row, -self.direction.col)
        
    def hit_ann(self, refl):
        self.direction = Point(0,0)
        
    def hit_line(self, refl):
        self.direction = refl
    
    def update(self):
        """Move position to next intersection point."""
        options = [ (p, d, None, self.hit_concave_corner) for (p,d) in self.find_corners() ]
        options.extend( (p, d, None, self.hit_ann) for (p,d) in self.find_ann_corners() )
        options.extend( (p, d, r, self.hit_line) for (p,d,r) in self.find_next_intersection() )
        d = self.can_hit_start()
        if d != -1:
            options.append( (self.hm.position, d, None, self.at_start) )
        p, d, r, action = min(options, key = lambda quad : quad[1])
        action(r)
        self.distance_travelled += self.distance(self.position, p)
        self.position = p

    def back_at_start(self):
        return self.position == self.hm.position

    def lost_ray(self):
        return self.direction.row == 0 and self.direction.col == 0
    
    def does_get_home(self, max_distance):
        """Returns true if can get back to start in <= max_distance."""
        epsilon = 1e-7
        while True:
            self.update()
            if self.distance_travelled >= epsilon + max_distance:
                return False
            if self.lost_ray():
                return False
            if self.back_at_start():
                return True
        return False

import fractions

class Affine:
    def __init__(self, p):
        self.point = p
        
    def normalform(self):
        """(x,y) can always be mapped to (1,0), (-1,0), (x,1) or (x,-1) by scaling by a strictly positive scalar."""
        if self.point.col == 0:
            if self.point.row > 0:
                return Point(1,0)
            return Point(-1,0)
        if self.point.col > 0:
            return Point(fractions.Fraction(self.point.row, self.point.col), 1)
        return Point(fractions.Fraction(self.point.row, -self.point.col), -1)
        
    def __eq__(self, other):
        snf = self.normalform()
        onf = other.normalform()
        return snf.col == onf.col and snf.row == onf.row
        
    def __hash__(self):
        return hash(self.normalform())
    
    def __repr__(self):
        return "Affine({},{})".format(self.point.row, self.point.col)

def find_directions(D):
    return set( Affine(Point(x,y)) for x in range(-D, D+1) for y in range(-D, D+1)
                if x * x + y * y <= D * D and x * x + y * y > 0 )

num_cases = int(input())
for case in range(1, num_cases+1):
    H, W, D = [int(x) for x in input().split()]
    maze = [input() for _ in range(H)]
    hm = HallMirrors(maze)
    count = 0
    for direction in find_directions(D):
        light = Light(direction.point, hm)
        if light.does_get_home(D):
            count += 1
    print("Case #{}: {}".format(case, count))
