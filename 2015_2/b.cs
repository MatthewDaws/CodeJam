using System;
using System.Diagnostics;
using System.Collections.Generic;
using System.Linq;
using System.Numerics; // Compile with "/r:System.Numerics.dll"

class Program
{
    static int Main()
    {
        //var a = new UpperHalfPlanePoint(249198980,102210652423264);
        //var b = new UpperHalfPlanePoint(165402632, 64349618877208);
        //Console.WriteLine(a.CompareTo(b));
        //Console.WriteLine(b.CompareTo(a));
        //return 0;


        //var input = new InputLinesFromList(new List<string>() { "1", "1 10.0000 50.0000", "0.2000 50.0000" }); // 50
        //var input = new InputLinesFromList(new List<string>() { "1", "2 30.0000 65.4321", "0.0001 50.0000", "100.0000 99.9000" }); // 207221.843687375
        var input = new InputLinesFromConsole();

        int numCases = int.Parse(input.GetLine());

        for (int ca = 1; ca <= numCases; ++ca)
        {
            var pool = new Pool(input);
            var answer = pool.Solve();
            if (answer == 0)
            {
                Console.WriteLine("Case #{0}: IMPOSSIBLE", ca);
            }
            else
            {
                Console.WriteLine("Case #{0}: {1}", ca, answer);
            }
        }
        return 0;
    }
}

abstract class InputLines
{
    internal abstract string GetLine();
}

class InputLinesFromConsole : InputLines
{
    internal override string GetLine()
    {
        return Console.ReadLine();
    }
}

class InputLinesFromList : InputLines
{
    private List<string> TheList;
    private int index;

    internal InputLinesFromList(List<string> list)
    {
        TheList = list;
        index = 0;
    }

    internal override string GetLine()
    {
        if ( TheList == null || index >= TheList.Count() )
        {
            throw new Exception("InputLinesFromList:: Buffer all used.");
        }
        return TheList[index++];
    }
}

// Class to store points in the upper half plane.  Our interest is in the unusual ordering.
struct UpperHalfPlanePoint : IComparable<UpperHalfPlanePoint>
{
    BigInteger x, y;
    public BigInteger X { get { return x; } }
    public BigInteger Y { get { return y; } }

    public UpperHalfPlanePoint(BigInteger x, BigInteger y)
    {
        if ( y<0 )
        {
            throw new Exception("UpperHalfPlanePoint: constructor called with negative y value.");
        }
        this.x = x; this.y = y;
    }

    public override string ToString()
    {
        return String.Format("UpperHalfPlanePoint({0},{1})", X, Y);
    }

    // Implicit conversion operator to Points.
    public static implicit operator Point(UpperHalfPlanePoint uhp)
    {
        return new Point(uhp.X, uhp.Y);
    }

    // Ordering.  Based on angle from +ve x-axis.
    public int CompareTo(UpperHalfPlanePoint rhs)
    {
        // (0,0) smaller than all
        if (X == 0 && Y == 0)
        {
            if (rhs.X == 0 && rhs.Y == 0) { return 0; }
            return -1;
        }
        if (rhs.X == 0 && rhs.Y == 0) { return 1; }
        if ( rhs.X < 0 )
        {
            if (X < 0) { return new UpperHalfPlanePoint(-rhs.X, rhs.Y).CompareTo(new UpperHalfPlanePoint(-X, Y));  }
            return -1;
        }
        if ( rhs.X == 0 )
        {
            if (X > 0) { return -1; }
            if (X < 0) { return 1; }
            if (Y < rhs.Y) { return -1; }
            if (Y > rhs.Y) { return 1; }
            return 0;
        }
        // So rhs.X > 0
        if (X <= 0) { return 1; }
        if ( Y * rhs.X < rhs.Y * X ) { return -1; }
        if ( Y * rhs.X > rhs.Y * X ) { return 1; }
        if (X < rhs.X) { return -1; }
        if (X > rhs.X) { return 1; }
        return 0;
    }
}

// Simple Point class.
struct Point
{
    BigInteger x, y;
    public BigInteger X { get { return x; } }
    public BigInteger Y { get { return y; } }

    public Point(BigInteger x, BigInteger y)
    {
        this.x = x; this.y = y;
    }

    public override string ToString()
    {
        return String.Format("Point({0},{1})", X, Y);
    }

    public static Point operator+(Point lhs, Point rhs)
    {
        return new Point(lhs.X+rhs.X, lhs.Y+rhs.Y);
    }
}

class Pool
{
    public long VolumeAim { get; private set; }
    public long TempAim { get; private set; }
    public List<Tuple<long, long>> Pipes { get; private set; }
    public int NumPipes { get { return Pipes.Count(); } }

    internal Pool(InputLines input)
    {
        var line = input.GetLine().Split();
        int numPipes = int.Parse(line[0]);
        var data = new List<string> { line[1], line[2] };
        for (int i = 0; i < numPipes; ++i)
        {
            line = input.GetLine().Split();
            data.Add(line[0]); data.Add(line[1]);
        }

        var asLongs = ScaleFloats(data);
        VolumeAim = asLongs[0];
        TempAim = asLongs[1];
        Pipes = new List<Tuple<long, long>>();
        for (int i=2; i<asLongs.Count(); i+=2)
        {
            Pipes.Add(Tuple.Create(asLongs[i], asLongs[i + 1]));
        }
        //Console.WriteLine("Pipes:");
        //foreach (var pair in Pipes) { Console.WriteLine(pair); }
    }

    // Returns 0 : The three points are colinear
    // -ve : `three` lies on the right of the line from `one` to `two`.
    // +ve : `three` lies on the left of the line from `one` to `two`.
    private static int Colinear(Point one, Point two, Point three)
    {
        var det = (two.X - one.X) * (three.Y - one.Y) - (two.Y - one.Y) * (three.X - one.X);
        //var ddet = ((double)two.X - (double)one.X) * ((double)three.Y - (double)one.Y) - ((double)two.Y - (double)one.Y) * ((double)three.X - (double)one.X);
        //Console.WriteLine("Colinear({0}, {1}, {2}) -> {3}, {4}", one, two, three, det, ddet);
        if (det < 0) { return -1; }
        if (det > 0) { return 1; }
        return 0;
    }

    // Implements the Graham scan algorithm to find the convex hull of the passed set of points.
    private static List<Point> FindExtremePoints(List<Point> points, bool leaveColinear = true)
    {
        // Find lower-left point
        Point lowerLeft = points[0];
        for (int i=1; i<points.Count(); ++i)
        {
            if ( points[i].Y < lowerLeft.Y || ( points[i].Y == lowerLeft.Y && points[i].X < lowerLeft.X ) )
            {
                lowerLeft = points[i];
            }
        }
        var inUHP = new List<UpperHalfPlanePoint>(
            from point in points
            select new UpperHalfPlanePoint(point.X - lowerLeft.X, point.Y - lowerLeft.Y)
            );
        inUHP.Sort();
        for (int i=1; i<inUHP.Count(); ++i)
        {
            if ( inUHP[i].CompareTo(inUHP[i-1]) < 0 )
            {
                //Console.WriteLine("inUHP:");
                //foreach (var pt in inUHP) { Console.WriteLine(pt); }
                throw new Exception("Doesn't appear to be sorted correctly!");
            }
        }
        // Check for and discard repeated points
        var uniques = new List<UpperHalfPlanePoint>();
        uniques.Add(inUHP[0]);
        for (int i=1; i<inUHP.Count(); ++i)
        {
            if ( inUHP[i].CompareTo(inUHP[i-1]) != 0 )
            {
                uniques.Add(inUHP[i]);
            }
        }
        inUHP = uniques;
        // Special case
        if ( inUHP.Count() <= 2 )
        {
            return new List<Point>(from uhp in inUHP select new Point(uhp.X + lowerLeft.X, uhp.Y + lowerLeft.Y));
        }
        // Now implement the Graham Scan algorithm
        var convexHull = new List<UpperHalfPlanePoint>();
        convexHull.Add(inUHP[0]);
        convexHull.Add(inUHP[1]);
        convexHull.Add(inUHP[2]);
        int index = 3;
        while (true)
        {
            int direction = Colinear(convexHull[convexHull.Count() - 3], convexHull[convexHull.Count() - 2],
                convexHull[convexHull.Count() - 1]);
            if (direction < 0 || (leaveColinear == false && direction == 0))
            {
                // Right turn, so reject -2 point
                convexHull.RemoveAt(convexHull.Count() - 2);
                // If we delete colinears then possible to run out of points!
                if (convexHull.Count() < 3)
                {
                    if (index == inUHP.Count()) { break; }
                    convexHull.Add(inUHP[index++]);
                }
            }
            else
            {
                if (index == inUHP.Count()) { break; }
                convexHull.Add(inUHP[index++]);
            }
        }
        return new List<Point>(from uhp in convexHull select new Point(uhp.X + lowerLeft.X, uhp.Y + lowerLeft.Y));
    }

    /// <summary>
    /// Finds if a line segment intersects with a ray from the origin
    /// </summary>
    /// <param name="seg0">Point object of one end of segment</param>
    /// <param name="seg1">Point object of one end of segment</param>
    /// <param name="vec">Point object representing the ray</param>
    /// <returns>The value of t>0 such that vec / t is on the segment, or 0 otherwise.</returns>
    private static double IntersectSegmentVector(Point seg0, Point seg1, Point vec)
    {
        var det = (seg1.X - seg0.X) * vec.Y - (seg1.Y - seg0.Y) * vec.X;
        //var ddet = ((double)seg1.X - (double)seg0.X) * (double)vec.Y - ((double)seg1.Y - (double)seg0.Y) * (double)vec.X;
        //Console.WriteLine("IntersectSegmentVector({0}, {1}, {2}) -> {3}, {4}", seg0, seg1, vec, det, ddet);
        if ( det == 0 )
        {
            if ( vec.X * seg0.Y == vec.Y * seg0.Y )
            {
                if ( seg0.X == 0 )
                {
                    if ( seg1.X == 0)
                    {
                        return 0;
                    }
                    return (double)vec.X / (double)seg1.X;
                }
                if ( seg1.X == 0 )
                {
                    return (double)vec.X / (double)seg0.X;
                }
                return Math.Min( (double)vec.X / (double)seg1.X, (double)vec.X / (double)seg0.X );
            }
            return 0;
        }
        //var s = ((double)vec.Y * (double)seg1.X - (double)vec.X * (double)seg1.Y) / (double)det;
        var s = (double)(vec.Y * seg1.X - vec.X * seg1.Y) / (double)det;
        if ( s<0 || s>1 ) { return 0; }
        var invt = (double)((seg0.Y - seg1.Y) * seg1.X - (seg0.X - seg1.X) * seg1.Y) / (double)det;
        if ( invt <= 0.0 ) { return 0; }
        return 1.0 / invt;
    }
    
    /// <summary>
    /// Finds the minimal value of t so that `vector`/t is in the convex hull
    /// </summary>
    /// <param name="convexHull">extreme points defining the convex hull.  First point should be (0,0)</param>
    /// <param name="vector">vector from origin</param>
    /// <returns>0 if no valid t</returns>
    private static double FindMinScale(List<Point> convexHull, Point vector)
    {
        if ( Colinear(convexHull[0], convexHull[1], vector) < 0 ) { return 0; }
        if ( Colinear(convexHull[0], convexHull[convexHull.Count() - 1], vector) > 0 ) { return 0; }
        double t = 0;
        double tnew;
        for (int i=0; i<convexHull.Count()-1; ++i)
        {
            tnew = IntersectSegmentVector( convexHull[i], convexHull[i+1], vector);
            if ( tnew != 0 && ( t==0 || tnew<t) )
            {
                t = tnew;
            }
        }
        tnew = IntersectSegmentVector( convexHull[convexHull.Count()-1], convexHull[0], vector);
        if ( tnew != 0 && ( t==0 || tnew<t) )
        {
            t = tnew;
        }
        return t;
    }

    /// <summary>
    /// Converts strings of floats to integers by multiplying by a factor of 10.
    /// </summary>
    /// <param name="data">List of input strings, which should be "12" or "5.230" but not exponential format.</param>
    /// <returns>List of longs</returns>
    static private List<long> ScaleFloats(List<string> data)
    {
        int scalePower = 0;
        foreach (string num in data)
        {
            var parts = num.Split(new char[] {'.'});
            if ( parts.Count() > 1 && parts[1].Length > scalePower )
            {
                scalePower = parts[1].Length;
            }
        }
        var newData = new List<long>();
        foreach (string num in data)
        {
            var parts = num.Split(new char[] { '.' });
            string asInt = ( parts.Count() > 1 ) ? parts[1] : "";
            for (int i=asInt.Length; i < scalePower; ++i)
            {
                asInt = asInt + "0";
            }
            newData.Add(long.Parse(parts[0] + asInt));
        }
        return newData;
    }
    
    internal double Solve()
    {
        var extremePoints = new List<Point> { new Point(0, 0) };
        //Console.WriteLine("Pipes:");
        //foreach (var pair in Pipes) { Console.WriteLine(pair); }
        foreach (var pair in Pipes)
        {
            var point = new Point(pair.Item1, pair.Item1 * pair.Item2);
            var points = new List<Point>(extremePoints);
            foreach (Point pt in extremePoints)
            {
                points.Add(pt + point);
            }
            extremePoints = FindExtremePoints(points, false);
            //Console.WriteLine("New extreme points...");
            //foreach (var pt in extremePoints) { Console.WriteLine(pt); }
        }
        var aim = new Point(VolumeAim, VolumeAim * TempAim);
        //Console.WriteLine("Aim: {0}", aim);
        return FindMinScale(extremePoints, aim);
    }

}
