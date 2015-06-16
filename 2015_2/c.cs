using System;
using System.Diagnostics;
using System.Collections.Generic;
using System.Linq;

using GraphPaths;

class Program
{
    static int Main()
    {
        //var input = new InputLinesFromList(new List<string>() { "2", "he loves to eat baguettes", "il aime manger des baguettes" });
        //int numCases = 1;

        var input = new InputLinesFromConsole();
        int numCases = int.Parse(input.GetLine());

        for (int ca = 1; ca <= numCases; ++ca)
        {
            var words = new Words(input);
            Console.WriteLine("Case #{0}: {1}", ca, words.Solve());
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

class Words
{
    readonly int _numLines;
    public int NumLines { get { return _numLines; } }

    // Interesting aside: this is very hard to make properly "readonly", see
    // http://blogs.msdn.com/b/ericlippert/archive/2007/11/13/immutability-in-c-part-one-kinds-of-immutability.aspx
    // Oh for C++ "const"...
    public List<HashSet<string>> Lines { get; private set; }

    public Words(InputLines input)
    {
        _numLines = int.Parse(input.GetLine());
        Lines = new List<HashSet<string>>();
        for (int i = 0; i < NumLines; ++i)
        {
            Lines.Add(new HashSet<string>(input.GetLine().Split()));
        }
    }

    private void DisplaySet<T>(HashSet<T> set)
    {
        Console.Write("{");
        foreach (T x in set) { Console.Write("{0}, ", x); }
        Console.Write("}\n");
    }

    public int Solve()
    {
        var allWords = new HashSet<string>(
            from line in Lines
            from word in line
            select word);
        var wordNum = new Dictionary<string, int>();
        int count = 0;
        foreach (var word in allWords)
        {
            wordNum[word] = count++;
        }
        var numLines = new List<HashSet<int>>(
            from line in Lines
            select new HashSet<int>(from word in line select wordNum[word]));

        var graph = new UndirectedGraph<int>();
        for (int i = 0; i < count; ++i)
        {
            for (int j = 0; j < count; ++j)
            {
                if (i != j && numLines.Any(line => line.Contains(i) & line.Contains(j)))
                {
                    graph.AddEdge(i, j);
                }
            }
        }

        // Add dummy vertices
        int englishClique = count;
        int frenchClique = count + 1;
        foreach (int i in numLines[0])
        {
            graph.AddEdge(englishClique, i); // English clique vertex
        }
        foreach (int i in numLines[1])
        {
            graph.AddEdge(frenchClique, i); // French clique vertex
        }

        // Count edges
        /*var vertices = new HashSet<int>(graph.DepthFirstSearch(count));
        Console.WriteLine("Vertices: {0}", vertices.Count());
        var edges = new HashSet<Tuple<int, int>>(
            from vertex in vertices
            from end in ((IGraphEdges<int>)graph).GetNeighbours(vertex)
            select Tuple.Create(vertex, end));
        Console.WriteLine("Edges: {0}", edges.Count());*/

        // Speed things up by adding paths we know must exist.
        // If word in both Lines[0] and Lines[1] then path
        var usedEdges = new HashSet<Tuple<int, int>>();
        var search = from i in numLines[0] where numLines[1].Contains(i) select i;
        var usedVertices = new HashSet<int>();
        foreach (int i in search)
        {
            usedEdges.Add(Tuple.Create(englishClique, i));
            usedEdges.Add(Tuple.Create(i, frenchClique));
            usedVertices.Add(i);
        }
        // If word1 in Lines[0] and Lines[k] but not in Lines[1],
        // and word2 in Lines[1] and Lines[k] but not in Lines[0],
        // then path englishClique -> word1 -> word2 -> frenchClique
        // Advantage here is that we _know_ Lines[k] is small
        for (int k = 2; k < numLines.Count(); ++k)
        {
            var search1 = from i1 in numLines[k] where numLines[0].Contains(i1) && !numLines[1].Contains(i1) select i1;
            var search2 = from i2 in numLines[k] where numLines[1].Contains(i2) && !numLines[0].Contains(i2) select i2;
            foreach (int i1 in search1)
            {
                foreach (int i2 in search2)
                {
                    if (!usedVertices.Contains(i1) && !usedVertices.Contains(i2))
                    {
                        usedVertices.Add(i1); usedVertices.Add(i2);
                        usedEdges.Add(Tuple.Create(englishClique, i1));
                        usedEdges.Add(Tuple.Create(i1, i2));
                        usedEdges.Add(Tuple.Create(i2, frenchClique));
                    }
                }
            }
        }

        return graph.FindVertexDisjointPaths1(englishClique, frenchClique, usedEdges).Count();
    }
}
