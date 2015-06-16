using System;
using System.Diagnostics;
using System.Collections.Generic;
using System.Linq;

using RateTemp = System.Tuple<double, double>;

class Program
{
    static int Main()
    {
        //var input = new InputLinesFromList(new List<string>() { "2", "2 4", "3 5" });
        var input = new InputLinesFromConsole();

        int numCases = int.Parse(input.GetLine());

        for (int ca = 1; ca <= numCases; ++ca)
        {
            var drum = new Drum(input);
            Console.WriteLine("Case #{0}: {1}", ca, drum.Solve());
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

static class SortedDictionaryExtension
{
    // Extension method to add to a Dictionary if key exists
    // Slightly silly use here, but shows the principle.
    // Annoyingly C# doesn't allow generics, as it can't verify that TValue supports "+".
    public static void BuildOrAdd(this SortedDictionary<int, long> sd, int key, long add, long start = 0)
    {
        if (!sd.ContainsKey(key)) { sd[key] = start; }
        sd[key] += add;
    }
}

class Drum
{
    public readonly int NumRows, NumCols;

    public Drum(InputLines input)
    {
        var data = input.GetLine().Split();
        NumRows = int.Parse(data[0]);
        NumCols = int.Parse(data[1]);
    }

    public long Solve()
    {
        // Dynamic programming.
        // This dictionary will contain the number of remaining rows left to consider, and a count
        // of the number of cases which lead to this case.  We'll fix the invariant that a rows of 3s
        // is always "next".
        // Reverse normal ordering, so largest number is "first".
        var toConsider = new SortedDictionary<int, long>(Comparer<int>.Create((a, b) => b - a));
        // Case when first row is a row of 3s
        toConsider[NumRows] = 1;
        // Case when first row is a row of "non-3s".
        var otherOptions = DynamicStep();
        foreach (int size in otherOptions)
        {
            toConsider.BuildOrAdd(NumRows - size, 1);
        }
        
        // Now descend
        do
        {
            var pair = toConsider.First();
            int rows = pair.Key;
            long count = pair.Value;
            if ( rows == 0 )
            {
                return count; // TODO: Modulo
            }
            toConsider.Remove(rows);
            // Add rows of 3s and an "other"
            // Special case: if only 2 rows remain, then a row of 3s will finish the pattern
            if (rows == 2)
            {
                toConsider.BuildOrAdd(0, count);
                toConsider[0] %= 1000000007;
            }
            foreach (int size in otherOptions)
            {
                toConsider.BuildOrAdd(rows - 2 - size, count);
                toConsider[rows - 2 - size] %= 1000000007;
            }
        } while (true);
    }

    // Return a list of options to explore from currentRows by adding a "non-3 row(s)"
    List<int> DynamicStep()
    {
        var options = new List<int> {1} ; // 22222222
        if ( NumCols % 3 == 0 )
        {
            options.Add(2); // 122
                            // 122
        }
        if ( NumCols % 6 == 0 )
        {
            options.Add(2); // 221122
                            // 122221
        }
        if ( NumCols % 4 == 0 )
        {
            options.Add(3); // 2122
                            // 2121
                            // 2221
        }
        return options;
    }
}