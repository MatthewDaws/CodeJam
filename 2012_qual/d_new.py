#from fractions import Fraction
import math
from collections import namedtuple
Point = namedtuple("Point", ["row","col"])

class Fraction:
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

    @staticmethod
    def gcd(a, b):
        while b:
            a, b = b, a%b
        return a

    def lowest_form(self):
        g = self.gcd(self.num, self.dem)
        self.num //= g
        self.dem //= g
    
    def __hash__(self):
        self.lowest_form()
        if self.dem == 1:
            return hash(self.num)
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


class BounceBox:
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction

    def __repr__(self):
        return "Pos: {} Dir: {}".format(self.position, self.direction)
        
    @staticmethod
    def distance(one, two):
        x = one.row - two.row
        y = one.col - two.col
        return math.sqrt( float(x*x + y*y) )

    def hit_point(self, p):
        """Returns distance to `p` or -1 if can't hit."""
        # Solve self.position + t * self.direction == p for t > 0
        if self.direction.row == 0:
            if p.row != self.position.row:
                return -1
            tcol = Fraction(p.col - self.position.col, self.direction.col)
            if tcol <= 0:
                return -1
            return self.distance(self.position, p)
        trow = Fraction(p.row - self.position.row, self.direction.row)
        if trow <= 0:
            return -1
        if self.direction.col == 0:
            if p.col != self.position.col:
                return -1
            return self.distance(self.position, p)
        tcol = Fraction(p.col - self.position.col, self.direction.col)
        if trow != tcol:
            return -1
        return self.distance(self.position, p)

    middle = Point(Fraction(1,2),Fraction(1,2))

    def update(self):
        """Move position to the boundary of the box, or to (1/2,1/2).
        Returns distance travelled."""
        # Can hit middle?
        d = self.hit_point(self.middle)
        if d != -1:
            self.position = self.middle
            return d
        # Hit corners
        #corners = [ Point(0,0), Point(1,0), Point(0,1), Point(1,1) ]
        #for p in corners:
        #    d = self.hit_point(p)
        #    if d != -1:
        #        self.travelled += d
        #        self.position = p
        #        return
        # Hit side?
        if self.direction.row == 0:
            col = 1 if self.direction.col > 0 else 0
            # Solve self.position.col + t * self.direction.col == col
            t = Fraction(col - self.position.col, self.direction.col)
            if t <= 0: raise Exception("Shouldn't happen 1")
            p = Point(self.position.row + t * self.direction.row, col)
            d = self.distance(p, self.position)
            self.position = p
            return d
        else:
            if self.direction.col == 0:
                row = 1 if self.direction.row > 0 else 0
                t = Fraction(row - self.position.row, self.direction.row)
                if t <= 0: raise Exception("Shouldn't happen 2")
                p = Point(row, self.position.col + t * self.direction.col)
                d = self.distance(p, self.position)
                self.position = p
                return d
            else:
                col = 1 if self.direction.col > 0 else 0
                tcol = Fraction(col - self.position.col, self.direction.col)
                if tcol <= 0: raise Exception("Shouldn't happen 3")
                row = 1 if self.direction.row > 0 else 0
                trow = Fraction(row - self.position.row, self.direction.row)
                if trow <= 0: raise Exception("Shouldn't happen 4")
                t = min(trow, tcol)
                p = Point(self.position.row + t * self.direction.row, self.position.col + t * self.direction.col)
                d = self.distance(p, self.position)
                self.position = p
                return d

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
                    self.position = Point(row, col)

    def __repr__(self):
        return "\n".join(self.maze) + "\nPosition: " + str(self.position)

    def at_corner(vec):
        return Point(-vec.row, -vec.col)
    def horz_refl(vec):
        return Point(-vec.row, vec.col)
    def vert_refl(vec):
        return Point(vec.row, -vec.col)
    def no_action(vec):
        return vec
    def absorb(vec):
        return Point(0,0)
    CornerData = namedtuple("CornerData", ["layout", "action"])
    corners = {Point(0,0) : CornerData([Point(-1,-1), Point(-1,0), Point(0,-1), Point(0,0)],
                                       {"###." : (at_corner, Point(0, 0)),
                                        "##.." : (horz_refl, Point(0, -1)),
                                        "#.#." : (vert_refl, Point(-1, 0)),
                                        "...." : (no_action, Point(-1, -1)),
                                        ".#.." : (no_action, Point(-1, -1)),
                                        "..#." : (no_action, Point(-1, -1)),
                                        ".##." : (no_action, Point(-1, -1)),
                                        "#..." : (absorb, Point(0, 0)) }
                                       ),
               Point(1,0) : CornerData([Point(0,-1), Point(0,0), Point(1,-1), Point(1,0)],
                                       {"...." : (no_action, Point(1, -1)),
                                        "#..." : (no_action, Point(1, -1)),
                                        "..#." : (absorb, Point(0, 0)),
                                        "...#" : (no_action, Point(1, -1)),
                                        "#.#." : (vert_refl, Point(1,0)),
                                        "#..#" : (no_action, Point(1, -1)),
                                        "..##" : (horz_refl, Point(0, -1)),
                                        "#.##" : (at_corner, Point(0, 0)) }
                                       ),
               Point(0,1) : CornerData([Point(-1,0), Point(-1,1), Point(0,0), Point(0,1)],
                                       {"...." : (no_action, Point(-1, 1)),
                                        "#..." : (no_action, Point(-1, 1)),
                                        ".#.." : (absorb, Point(0, 0)),
                                        "...#" : (no_action, Point(-1, 1)),
                                        "##.." : (horz_refl, Point(0, 1)),
                                        "#..#" : (no_action, Point(-1, 1)),
                                        ".#.#" : (vert_refl, Point(-1, 0)),
                                        "##.#" : (at_corner, Point(0, 0)) }
                                       ),
               Point(1,1) : CornerData([Point(0,0), Point(0,1), Point(1,0), Point(1,1)],
                                       {"...." : (no_action, Point(1, 1)),
                                        ".#.." : (no_action, Point(1, 1)),
                                        "..#." : (no_action, Point(1, 1)),
                                        "...#" : (absorb, Point(0, 0)),
                                        ".##." : (no_action, Point(1, 1)),
                                        ".#.#" : (vert_refl, Point(1, 0)),
                                        "..##" : (horz_refl, Point(0, 1)),
                                        ".###" : (at_corner, Point(0, 0)) }
                                       )
               }

                    
    def reflect(self, bb, gridpoint):
        """bb = BounceBox object.  Reflects based on bb state, where `gridpoint` is the square we're in.
        Returns a pair (new_bb, new_gridpoint)
        If new_bb.direction == Point(0,0) then the light ray has been absorbed."""
        # If at (0,0) then look at ??  -->  ##   ##   #.   ..  .#  ..  .#   #.
        #                          ?X       #.   ..   #.   ..  ..  #.  #.   ..
        #       (1,0) then look at ?X  -->  ..  #.  ..  ..  #.  #.  ..  #.
        #                          ??       ..  ..  #.  .#  #.  .#  ##  ##
        #       (0,1) then look at ??  -->  ..  #.  .#  ..  ##  #.  .#  ##
        #                          X?       ..  ..  ..  .#  ..  .#  .#  .#
        #       (1,1) then look at X?  -->  ..  .#  ..  ..  .#  .#  ..  .#
        #                          ??       ..  ..  #.  .#  #.  .#  ##  ##
        if bb.position in HallMirrors.corners:
            c = HallMirrors.corners[bb.position]
            layout = "".join( self.maze[gridpoint.row + x.row][gridpoint.col + x.col]
                             for x in c.layout )
            action, delta = c.action[layout]
            #print("At corner:", action, delta)
            newdir = action(bb.direction)
            #if newdir != bb.direction:
            #    return BounceBox(bb.position, newdir), gridpoint
            return (BounceBox(Point(bb.position.row - delta.row, bb.position.col - delta.col), newdir),
                    Point(gridpoint.row + delta.row, gridpoint.col + delta.col) )
        # Otherwise hit a side
        if bb.position.row == 0:
            if self.maze[gridpoint.row - 1][gridpoint.col] == "#":
                return BounceBox(bb.position, HallMirrors.horz_refl(bb.direction)), gridpoint
            return BounceBox(Point(1, bb.position.col), bb.direction), Point(gridpoint.row - 1, gridpoint.col)
        if bb.position.row == 1:
            if self.maze[gridpoint.row + 1][gridpoint.col] == "#":
                return BounceBox(bb.position, HallMirrors.horz_refl(bb.direction)), gridpoint
            return BounceBox(Point(0, bb.position.col), bb.direction), Point(gridpoint.row + 1, gridpoint.col)
        if bb.position.col == 0:
            if self.maze[gridpoint.row][gridpoint.col - 1] == "#":
                return BounceBox(bb.position, HallMirrors.vert_refl(bb.direction)), gridpoint
            return BounceBox(Point(bb.position.row, 1), bb.direction), Point(gridpoint.row, gridpoint.col - 1)
        if bb.position.col == 1:
            if self.maze[gridpoint.row][gridpoint.col + 1] == "#":
                return BounceBox(bb.position, HallMirrors.vert_refl(bb.direction)), gridpoint
            return BounceBox(Point(bb.position.row, 0), bb.direction), Point(gridpoint.row, gridpoint.col + 1)
        raise Exception("Shouldn't get here 1")

def trace_path(hm, direction, maxdist):
    bb = BounceBox(BounceBox.middle, direction)
    gridpoint = hm.position
    travelled = 0
    while True:
        #print("Before:", bb)
        travelled += bb.update()
        #print("After:", bb)
        if travelled > maxdist + 1e-6:
            return False
        if bb.position == BounceBox.middle:
            if gridpoint == hm.position:
                return True
            #print("2 Before:", bb)
            travelled += bb.update()
            #print("2 After:", bb)
            if travelled > maxdist + 1e-6:
                return False
        bb, gridpoint = hm.reflect(bb, gridpoint)
        if bb.direction == Point(0,0):
            return False
        #print("({},{}) {} {}".format(gridpoint.row + bb.position.row,
        #                             gridpoint.col + bb.position.col, bb.direction, travelled))

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
        if trace_path(hm, direction.point, D):
            count += 1
    print("Case #{}: {}".format(case, count))
