using System;
using System.Diagnostics;
using System.Collections.Generic;
using System.Linq;

class Program
{
    static int Main()
    {
        //var input = new InputLinesFromList(new List<string>() { "1", "1 10.0000 50.0000", "0.2000 50.0000" });
        //var input = new InputLinesFromList(new List<string>() { "1", "2 30.0000 65.4321", "0.0001 50.0000", "100.0000 99.9000" });
        //var input = new InputLinesFromList(new List<string>() { "1", "2 5.0000 99.9000", "30.0000 99.8999", "20.0000 99.7000" });
        //var input = new InputLinesFromList(new List<string>() { "1", "2 0.0001 0.1000", "0.0001 0.1002", "0.0001 0.1001" });
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
        for (int i = 2; i < asLongs.Count(); i += 2)
        {
            Pipes.Add(Tuple.Create(asLongs[i], asLongs[i + 1]));
        }
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
            var parts = num.Split(new char[] { '.' });
            if (parts.Count() > 1 && parts[1].Length > scalePower)
            {
                scalePower = parts[1].Length;
            }
        }
        var newData = new List<long>();
        foreach (string num in data)
        {
            var parts = num.Split(new char[] { '.' });
            string asInt = (parts.Count() > 1) ? parts[1] : "";
            for (int i = asInt.Length; i < scalePower; ++i)
            {
                asInt = asInt + "0";
            }
            newData.Add(long.Parse(parts[0] + asInt));
        }
        return newData;
    }

    internal double Solve()
    {
        // Find best flow rates
        var flowRates = new List<double>(from pair in Pipes select (double)pair.Item1);
        var constraints = new List<long>(from pair in Pipes select pair.Item2 - TempAim);
        // Ensure positive
        double sum = flowRates.Zip(constraints, (f, c) => f * (double)c).Sum();
        if ( sum < 0 )
        {
            for (int i = 0; i < constraints.Count(); ++i) { constraints[i] = -constraints[i]; }
        }
        // Now solve
        while (true)
        {
            // Decrease from maximum
            int maxIndex = -1;
            long maxConstraint = 0;
            for (int i = 0; i < flowRates.Count(); ++i)
            {
                if (flowRates[i] > 0)
                {
                    if (maxIndex == -1 || constraints[i] > maxConstraint)
                    {
                        maxIndex = i; maxConstraint = constraints[i];
                    }
                }
            }
            //Console.WriteLine("Decrease index {0}", maxIndex);
            if (maxIndex == -1) { return -1; } // No non-zero answer
            // How much to decrease?
            sum = flowRates.Zip(constraints, (f, c) => f * (double)c).Sum();
            double decrease = sum == 0 ? 0 : sum / maxConstraint;
            //Console.WriteLine("sum:{0} maxConstraint:{1} --> {2}", sum, maxConstraint, decrease);
            if ( decrease <= flowRates[maxIndex] )
            {
                flowRates[maxIndex] -= decrease;
                // Done, so return
                sum = flowRates.Sum();
                if (sum == 0) { return -1; }
                return VolumeAim / sum;
            }
            else
            {
                flowRates[maxIndex] = 0; // Must now continue
            }
        }
    }
}