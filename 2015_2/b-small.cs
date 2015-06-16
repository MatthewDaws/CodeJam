using System;
using System.Diagnostics;
using System.Collections.Generic;
using System.Linq;

using RateTemp = System.Tuple<double, double>;

class Program
{
    static int Main()
    {
        //var input = new InputLinesFromList(new List<string>() { "1", "1 10.0000 50.0000", "0.2000 50.0000" });
        //var input = new InputLinesFromList(new List<string>() { "1", "2 30.0000 65.4321", "0.0001 50.0000", "100.0000 99.9000" });
        var input = new InputLinesFromConsole();

        int numCases = int.Parse(input.GetLine());

        for (int ca = 1; ca <= numCases; ++ca)
        {
            var pool = new Pool(input);
            var answer = pool.Solve();
            if (answer < 0)
            {
                Console.WriteLine("Case #{0}: IMPOSSIBLE", ca);
            }
            else
            {
                Console.WriteLine("Case #{0}: {1}", ca, pool.Solve());
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

class Pool
{
    public double VolumeAim { get; private set; }
    public double TempAim { get; private set; }
    public List<RateTemp> Pipes { get; private set; }
    private List<double> x, y;
    public int NumPipes { get { return Pipes.Count(); } }

    internal Pool(InputLines input)
    {
        var line = input.GetLine().Split();
        int numPipes = int.Parse(line[0]);
        VolumeAim = double.Parse(line[1]);
        TempAim = double.Parse(line[2]);
        Pipes = new List<RateTemp>();
        x = new List<double>();
        y = new List<double>();
        for (int i = 0; i < numPipes; ++i)
        {
            line = input.GetLine().Split();
            double R = double.Parse(line[0]);
            double T = double.Parse(line[1]);
            Pipes.Add( new RateTemp(R, T) );
            double xx = R / VolumeAim;
            x.Add(xx);
            y.Add(xx * (T / TempAim));
        }
    }

    internal double Solve()
    {
        if (NumPipes == 1) { return Solve1(); }
        if (NumPipes == 2) { return Solve2(); }
        throw new Exception("Cannot handle more than 2 input pipes.");
    }

    double Solve1()
    {
        if (x[0] != y[0]) {
            if (Math.Abs(x[0] - y[0]) < 1e-5)
            {
                Console.WriteLine("WARNING: {0}, {1}", x[0], y[0]);
            }
            return -1.0;
        }
        return 1.0 / x[0];
    }

    double Solve2()
    {
        if ( x[0]*y[1] == x[1]*y[0] )
        {
            if ( x[0] == y[0] )
            {
                return 1.0 / (x[0] + x[1]);
            }
            return -1;
        }
        double det = x[0]*y[1] - x[1]*y[0];
        double t1 = (y[1] - x[1]) / det;
        double t2 = (x[0] - y[0]) / det;
        if ( t1>=0 && t2>=0 )
        {
            return Math.Max(t1,t2);
        }
        return -1.0;
    }
}