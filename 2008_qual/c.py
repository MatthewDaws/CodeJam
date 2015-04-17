import math

class CircleIntersection:
    def __init__(self, radius):
        self.radius = radius
        self.radiussq = radius * radius
        
    def half_segment_area(self, d):
        """Area of (half of) a segment, where d is the "height" above the centre."""
        ratio = d / self.radius
        theta = 2 * math.acos(ratio)
        sintheta = 2 * ratio * math.sqrt(1 - ratio*ratio)
        return self.radius * self.radius * (theta - sintheta) * 0.25

    def area_intersect_square(self, x, y, g):
        """Assumes x>=0, y>=0.  Area of intersection of the circle with square with corners
        (x, y) and (x+hg, y+g), and sides parallel to the axes."""
        dist_near_corner = x*x + y*y
        dist_far_corner = (x+g)**2 + (y+g)**2
        dist_top_corner = x*x + (y+g)**2
        dist_right_corner = (x+g)**2 + y*y
        if dist_near_corner >= self.radiussq:
            return 0
        if dist_far_corner <= self.radiussq:
            return g*g
        if dist_top_corner > self.radiussq and dist_right_corner <= self.radiussq:
            return self.half_segment_area(x) - self.half_segment_area(x+g) - g*y
        if dist_top_corner > self.radiussq and dist_right_corner > self.radiussq:
            delta = math.sqrt(self.radiussq - y*y)
            return self.half_segment_area(x) - self.half_segment_area(delta) - (delta - x) * y
        if dist_top_corner <= self.radiussq and dist_right_corner <= self.radiussq:
            delta = math.sqrt(self.radiussq - (y+g)**2)
            return g*(delta - x) + self.half_segment_area(delta) - self.half_segment_area(x+g) - (x + g - delta) * y
        delta1 = math.sqrt(self.radiussq - (y+g)**2)
        delta2 = math.sqrt(self.radiussq - y*y)
        return g*(delta1 - x) + self.half_segment_area(delta1) - self.half_segment_area(delta2) - (delta2 - delta1) * y

def area_missed(R,t,r,g):
    whole_sq_count = 0
    areas = []
    ci = CircleIntersection(R-t)
    # Limit calculation
    # min_x = r
    # y = r + m * (g + r + r)
    # want min_x*min_x + y*y >= (R-t)**2
    # <=> (r + m * (g + r + r))**2 >= (R-t)**2 - r**2
    # <=> m * (g + r + r) >= math.sqrt( (R-t)**2 - r**2 ) - r
    # <=> m >= ( math.sqrt( (R-t)**2 - r**2 ) - r ) / (g + r + r)
    limit = math.ceil( ( math.sqrt( (R-t)**2 - r**2 ) - r ) / (g + r + r) + 0.01 )
    for m in range(limit+1):
        y = r + m * (g + r + r)
        n = 0
        while True:
            x = r + n * (g + r + r)
            if x*x + y*y >= (R-t)**2:
                break
            if (x+g)**2 + (y+g)**2 <= (R-t)**2:
                whole_sq_count += 1
            else:
                areas.append(ci.area_intersect_square(x,y,g))
            n += 1
    # Worry about round-off
    areas.sort()
    return sum(areas) + whole_sq_count * g * g
    
# Read in setup
cases = int( input() )
for case in range(1,cases+1):
    f, R, t, r, g = [float(x) for x in input().split()]
    t += f
    g -= 2*f
    r += f
    if g <= 0.0:
        prob = 1.0
    else:
        prob = 1.0 - area_missed(R,t,r,g) * 4.0 / ( math.pi * R * R)
    print("Case #{}: {:.6f}".format(case, prob))
