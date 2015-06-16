class UpperHalfPlanePoint:
    def __init__(self, x, y):
        self.x, self.y = x, y
        
    def __repr__(self):
        return "UpperHalfPlanePoint({},{})".format(self.x, self.y)
        
    def __le__(self, rhs):
        # Special case is that (0,0) is the "smallest", so effectively (infty, 0)
        if self.x == 0 and self.y == 0:
            return True
        if rhs.x == 0 and rhs.y == 0:
            return False
        if rhs.x < 0:
            if self.x < 0:
                return UpperHalfPlanePoint(-rhs.x, rhs.y) <= UpperHalfPlanePoint(-self.x, self.y)
            return True
        if rhs.x == 0:
            if self.x > 0:
                return True
            if self.x < 0:
                return False
            return self.y <= rhs.y
        # So now rhs.x > 0
        if self.x <= 0:
            return False
        #slope1 = self.y / self.x
        #slope2 = rhs.y / rhs.x
        #if slope1 < slope2:
        #    return True
        #if slope1 > slope2:
        #    return False
        if self.y * rhs.x < rhs.y * self.x:
            return True
        if self.y * rhs.x > rhs.y * self.x:
            return False
        return self.x <= rhs.x
        
    def __eq__(self, rhs):
        return self <= rhs and rhs <= self
    
    def __ge__(self, rhs):
        return rhs <= self
    
    def __lt__(self, rhs):
        return self <= rhs and not rhs <= self
    
    def __gt__(self, rhs):
        return rhs < self
    
    def __ne__(self, rhs):
        return not self <= rhs or not rhs <= self
        
from collections import namedtuple
Point = namedtuple("Point", ["x", "y"])

def colinear(one, two, three):
    """Considers the vectors from one--two and one--three.  Returns:
    0 to indicate colinear
    -ve to indicate three lies on the right of the half-plane from one to two.
    +ve shows on the left."""
    return (two.x-one.x) * (three.y-one.y) - (two.y-one.y) * (three.x-one.x)

def FindExtremePoints(points, leaveColinear = True):
    lowerLeft = points[0]
    for point in points:
        if point.y < lowerLeft.y or ( point.y == lowerLeft.y and point.x < lowerLeft.x ):
            lowerLeft = point
    inUHP = [ UpperHalfPlanePoint(pt.x - lowerLeft.x, pt.y - lowerLeft.y) for pt in points ]
    inUHP.sort()
    #print(points, "-->", lowerLeft)
    #print(inUHP)
    # Need to check for repeated points
    uniques = [inUHP[0]]
    index = 1
    for index in range(1, len(inUHP)):
        if inUHP[index] != inUHP[index - 1]:
            uniques.append(inUHP[index])
    inUHP = uniques
    if len(inUHP) <= 2:
        return [ Point(pt.x + lowerLeft.x, pt.y + lowerLeft.y) for pt in inUHP ]
    # Now implement the Graham Scan algorithm
    convexHull = [inUHP[0], inUHP[1], inUHP[2]]
    index = 3
    while True:
        #direction = ( (convexHull[-2].x - convexHull[-3].x) * (convexHull[-1].y - convexHull[-3].y)
        #             - (convexHull[-2].y - convexHull[-3].y) * (convexHull[-1].x - convexHull[-3].x) )
        direction = colinear(convexHull[-3], convexHull[-2], convexHull[-1])
        if direction < 0 or (leaveColinear == False and direction == 0):
            # Right turn, so reject -2 point
            #print(convexHull[-3], convexHull[-2], convexHull[-1], "Right")
            del convexHull[-2]
            #newBack = convexHull.pop()
            #convexHull.pop()
            #convexHull.append(newBack)
            # If we delete colinears then possible to run out of points!
            if len(convexHull) < 3:
                if index == len(inUHP):
                    break
                convexHull.append( inUHP[index] )
                index += 1
        else:
            #print(convexHull[-3], convexHull[-2], convexHull[-1], "Left")
            if index == len(inUHP):
                break
            convexHull.append( inUHP[index] )
            index += 1

    return [ Point(pt.x + lowerLeft.x, pt.y + lowerLeft.y) for pt in convexHull ]
    
def IntersectSegmentVector(seg0, seg1, vec):
    """Finds if the line segment from `seg0` to `seg1` intersects the
    half-line in the direction of `vec`.  Returns the value of t>0 with
    vec / t in the line segment, or 0."""
    det = (seg1.x - seg0.x) * vec.y - (seg1.y - seg0.y) * vec.x
    if det == 0:
        if vec.x * seg0.y == vec.y * seg0.x:
            if seg0.x == 0:
                if seg1.x == 0:
                    return 0
                return vec.x / seg1.x
            if seg1.x == 0:
                return vec.x / seg0.x
            return min( vec.x / seg0.x, vec.x / seg1.x )
        return 0
    s = (vec.y * seg1.x - vec.x * seg1.y) / det
    if s < 0 or s > 1:
        return 0
    invt = ( (seg0.y - seg1.y) * seg1.x - (seg0.x - seg1.x) * seg1.y ) / det
    if invt <= 0:
        return 0
    return 1 / invt
    
def FindMinScale(convexHull, vector):
    """Input: convexHull is a list of extreme points of a convex set.
    Assumes convexHull[0] = Point(0,0) and ordering is counter-clockwise.
    Find the minimal t so that vector / t is in convexHull
    Returns 0 if t = infinity is the answer."""
    if colinear(convexHull[0], convexHull[1], vector) < 0:
        return 0
    if colinear(convexHull[0], convexHull[-1], vector) > 0:
        return 0
    t = 0
    for i in range(len(convexHull)-1):
        tnew = IntersectSegmentVector( convexHull[i], convexHull[i+1], vector)
        if tnew != 0 and ( t == 0 or tnew < t ):
            t = tnew
    tnew = IntersectSegmentVector( convexHull[-1], convexHull[0], vector)
    if tnew != 0 and ( t == 0 or tnew < t ):
        t = tnew
    return t
    
def ScaleFloats(data):
    """Pass a list of floating point numbers, as strings of the from "12" or "5.2300"
    but _not_ exponential format.  Finds a power of 10 to multiply them all by so they
    become integers, and returns this list of integers."""
    dataParts = [ x.split(".") for x in data ]
    scalePower = [len(x[1]) for x in dataParts if len(x) > 1]
    scalePower = max(scalePower) if len(scalePower) > 0 else 0
    newData = []
    for x in dataParts:
        b = x[1] if len(x) > 1 else ""
        b = b + "0"*(scalePower - len(b))
        newData.append( int(x[0] + b) )
    return newData
    
numCases = int(input())
for case in range(1, numCases+1):
    data = input().split()
    N = int(data[0])
    
    data = [data[1], data[2]]
    for _ in range(N):
        data.extend(input().split())
    data = ScaleFloats(data)
    V, X = data[0], data[1]
    R, C = data[2::2], data[3::2]
    
    extpts = [Point(0,0)]
    data = [ (r, r*c) for (r,c) in zip(R,C) ]
    for (x,y) in data:
        pt = Point(x, y)
        points = extpts[:] + [Point(p.x + pt.x, p.y + pt.y) for p in extpts]
        extpts = FindExtremePoints( points, False )
    aim = Point(V, V*X)
    T = FindMinScale(extpts, Point(aim[0], aim[1]))
	
    if T == 0:
        print("Case #{}: IMPOSSIBLE".format(case))
    else:
        print("Case #{}: {}".format(case, T))
