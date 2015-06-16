using System;
using System.Diagnostics;
using System.Collections.Generic;
using System.Linq;

class Program
{
    static int Main()
    {
        int numCases = int.Parse(Console.ReadLine());

        /*var maze = new PegMan(new string[] { "^", "^" });
        maze.PrintMaze();
        Console.WriteLine("Should be TFFT.");
        Console.WriteLine(maze.HitsEdgeWalker(new PegMan.Coord(0, 0), new PegMan.Coord(-1, 0)));
        Console.WriteLine(maze.HitsEdgeWalker(new PegMan.Coord(0, 0), new PegMan.Coord(1, 0)));
        Console.WriteLine(maze.HitsEdgeWalker(new PegMan.Coord(1, 0), new PegMan.Coord(-1, 0)));
        Console.WriteLine(maze.HitsEdgeWalker(new PegMan.Coord(1, 0), new PegMan.Coord(1, 0)));
        Console.WriteLine("Should be opposite.");
        Console.WriteLine(maze.HitsOther(new PegMan.Coord(0, 0), new PegMan.Coord(-1, 0)));
        Console.WriteLine(maze.HitsOther(new PegMan.Coord(0, 0), new PegMan.Coord(1, 0)));
        Console.WriteLine(maze.HitsOther(new PegMan.Coord(1, 0), new PegMan.Coord(-1, 0)));
        Console.WriteLine(maze.HitsOther(new PegMan.Coord(1, 0), new PegMan.Coord(1, 0)));
        Console.WriteLine("Should be TT");
        Console.WriteLine(maze.CanHitOther(new PegMan.Coord(0, 0)));
        Console.WriteLine(maze.CanHitOther(new PegMan.Coord(1, 0)));
        Console.WriteLine("SHould be 1: {0}", maze.SolveMaze());
        return 0;*/

        for (int ca = 1; ca <= numCases; ++ca)
        {
            var maze = new PegMan();
            maze.ReadFromConsole();
            int res = maze.SolveMaze();
            if (res == -1)
            {
                Console.WriteLine("Case #{0}: IMPOSSIBLE", ca);
            }
            else
            {
                Console.WriteLine("Case #{0}: {1}", ca, maze.SolveMaze());
            }
        }
        return 0;
    }
}

class PegMan
{
    private List<List<Directions.Dirs>> Maze { get; set; }
    private int NumRows
    {
        get
        {
            if (Maze == null) { return 0; }
            return Maze.Count();
        }
    }
    private int NumCols
    {
        get
        {
            if (Maze == null || Maze.Count() == 0) { return 0; }
            return Maze[0].Count();
        }
    }

    internal PegMan() { }

    internal PegMan(string[] initmaze)
    {
        Maze = new List<List<Directions.Dirs>>();
        foreach (var line in initmaze)
        {
            var rowDirs = line.Select(ch => Directions.Parse(ch));
            Maze.Add(rowDirs.ToList());
        }
    }

    internal void ReadFromConsole()
    {
        var rowCol = Console.ReadLine().Split(null);
        int numRowsTemp = int.Parse(rowCol[0]);
        int numColsTemp = int.Parse(rowCol[1]);

        Maze = new List<List<Directions.Dirs>>();
        for (int row = 0; row < numRowsTemp; ++row)
        {
            var line = Console.ReadLine();
            // Do this using simple LINQ
            IEnumerable<Directions.Dirs> rowDirs = line.Select(ch => Directions.Parse(ch));
            Maze.Add(rowDirs.ToList());
        }
    }

    internal int SolveMaze()
    {
        // Look at those points which current walk into the edge
        // These all need to be changed.  Can be done if each can be made to point at
        // another grid point which is not "."
        int count = 0;
        for (int row = 0; row < NumRows; ++row)
        {
            for (int col = 0; col < NumCols; ++col)
            {
                var place = new Coord(row, col);
                if ( HitsEdge(place) )
                {
                    ++count;
                    if ( !CanHitOther(place) ) { return -1; }
                }
            }
        }
        return count;
    }

    private bool CanHitOther(Coord place)
    {
        return HitsOther(place, new Coord(1, 0)) || HitsOther(place, new Coord(-1, 0))
            || HitsOther(place, new Coord(0, 1)) || HitsOther(place, new Coord(0, -1));
    }

    private bool HitsOther(Coord place, Coord direction)
    {
        return ! HitsEdgeWalker(place, direction);
    }

    private bool HitsEdge(Coord place)
    {
        switch ( Maze[place.Row][place.Col] )
        {
            case Directions.Dirs.Up:
                return HitsEdgeWalker(place, new Coord(-1, 0));
            case Directions.Dirs.Down:
                return HitsEdgeWalker(place, new Coord(1, 0));
            case Directions.Dirs.Left:
                return HitsEdgeWalker(place, new Coord(0, -1));
            case Directions.Dirs.Right:
                return HitsEdgeWalker(place, new Coord(0, 1));
            default:
                return false;
        }
    }

    private bool HitsEdgeWalker(Coord place, Coord delta)
    {
        place += delta;
        while ( place.Row >= 0 && place.Col >= 0 && place.Row < NumRows && place.Col < NumCols )
        {
            if (Maze[place.Row][place.Col] != Directions.Dirs.None) { return false; }
            place += delta;
        }
        return true;
    }

    internal void PrintMaze()
    {
        Console.WriteLine("Maze as read in:");
        var printDirs = new Dictionary<Directions.Dirs, string>{
            {Directions.Dirs.Up,    "up    "},
            {Directions.Dirs.Down,  "down  "},
            {Directions.Dirs.Left,  "left  "},
            {Directions.Dirs.Right, "right "},
            {Directions.Dirs.None,  "      "}
        };
        foreach (var row in Maze)
        {
            foreach (var entry in row) { Console.Write(printDirs[entry]); }
            Console.Write("\n");
        }
    }

    internal class Directions
    {
        internal static Dirs Parse(char ch)
        {
            switch (ch) {
                case '^': return Dirs.Up;
                case 'v': return Dirs.Down;
                case '<': return Dirs.Left;
                case '>': return Dirs.Right;
                case '.': return Dirs.None;
                default: throw new Exception("Unknown direction");
            }
        }
        internal enum Dirs { Up, Down, Left, Right, None };
    };

    internal struct Coord : IEquatable<Coord>
    {
        public readonly int Row, Col;
        public Coord(int row, int col)
        {
            Row = row; Col = col;
        }
        public static Coord operator +(Coord one, Coord two)
        {
            return new Coord(one.Row + two.Row, one.Col + two.Col);
        }

        // For fun, following MSDN recommendations
        public override bool Equals(Object obj)
        {
            return (obj is Coord && this == (Coord)obj);
        }

        public bool Equals(Coord other)
        {
            return this == other;
        }

        public static bool operator==(Coord lhs, Coord rhs)
        {
            return lhs.Row == rhs.Row && lhs.Col == rhs.Col;
        }

        public static bool operator!=(Coord lhs, Coord rhs)
        {
            return !(lhs == rhs);
        }

        public override int GetHashCode()
        {
            return new {Row, Col}.GetHashCode(); // Use anonymous type's default HashCode; slow but easy
        }

    }
}
