// - Simple Graph Interface
// - Find maximal number of edge-disjoint paths
// - Find maximal number of path-disjoint paths

using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace GraphPaths
{

    public interface IGraphEdges<T>
    {
        bool IsNeighbour(T vertex, T possibleNeighbour);
        IEnumerable<T> GetNeighbours(T vertex);
        // Interpret the edge `from -- to` as a (set of) directed edges:
        //   A directed graph would return just (from, to)
        //   but an undirected graph would return (from, to) and (to, from)
        IEnumerable<Tuple<T, T>> AsDirectedEdges(T from, T to);
    }

    // Simple directed graph class
    //   - Stores a dictionary of neighbours; though this is an implementation detail.
    public class DirectedGraph<T> : IGraphEdges<T>
    {
        private Dictionary<T, HashSet<T>> Neighbours;

        public DirectedGraph()
        {
            Neighbours = new Dictionary<T, HashSet<T>>();
        }

        public void AddEdge(T from, T to)
        {
            if (!Neighbours.ContainsKey(from))
            {
                Neighbours[from] = new HashSet<T>();
            }
            Neighbours[from].Add(to);
        }

        public void AddEdges(T[] edges)
        {
            for (int i = 0; i < edges.Count(); i += 2)
            {
                AddEdge(edges[i], edges[i + 1]);
            }
        }

        public void AddEdges(IEnumerable<Tuple<T, T>> edges)
        {
            foreach (var edge in edges) { AddEdge(edge.Item1, edge.Item2); }
        }

        public bool RemoveEdge(T from, T to)
        {
            if (Neighbours.ContainsKey(from))
            {
                return Neighbours[from].Remove(to);
            }
            return false;
        }

        public void RemoveVertex(T v)
        {
            Neighbours.Remove(v);
            foreach (var u in Neighbours.Keys)
            {
                Neighbours[u].Remove(v);
            }
        }

        public IEnumerable<Tuple<T, T>> Edges
        {
            get
            {
                foreach (var vertex in Neighbours.Keys)
                {
                    foreach (var v in Neighbours[vertex])
                    {
                        yield return Tuple.Create(vertex, v);
                    }
                }
            }
        }

        public override string ToString()
        {
            var ret = new StringBuilder();
            ret.AppendFormat("DirectedGraph<{0}>: ", typeof(T).Name);
            var ourEdges = new List<Tuple<T, T>>();
            foreach (Tuple<T, T> edge in Edges)
            {
                ret.AppendFormat("{0}->{1} ", edge.Item1, edge.Item2);
            }
            return ret.ToString();
        }

        bool IGraphEdges<T>.IsNeighbour(T vertex, T possibleNeighbour)
        {
            if (Neighbours.ContainsKey(vertex) && Neighbours[vertex].Contains(possibleNeighbour))
            {
                return true;
            }
            return false;
        }

        IEnumerable<T> IGraphEdges<T>.GetNeighbours(T vertex)
        {
            if (!Neighbours.ContainsKey(vertex)) { yield break; }
            foreach (T v in Neighbours[vertex])
            {
                yield return v;
            }
            /* Could also do the following, making use of the fact a HashSet is already Enumerable.
            if ( !Neighbours.ContainsKey(vertex) )
            {
                return Enumerable.Empty<T>();
            }
            return Neighbours[vertex];*/
        }

        IEnumerable<Tuple<T, T>> IGraphEdges<T>.AsDirectedEdges(T from, T to)
        {
            yield return Tuple.Create(from, to);
        }
    }

    // Undirected variant.
    //   - Decided not to subclass: it doesn't make any sense to treat an UndirectedGraph as Directed.
    //   - So a "has a" not an "is a".
    public class UndirectedGraph<T> : IGraphEdges<T>
    {
        private DirectedGraph<T> DGraph;

        public UndirectedGraph()
        {
            DGraph = new DirectedGraph<T>();
        }

        public void AddEdge(T from, T to)
        {
            DGraph.AddEdge(from, to);
            DGraph.AddEdge(to, from);
        }

        public void AddEdges(T[] edges)
        {
            for (int i = 0; i < edges.Count(); i += 2)
            {
                AddEdge(edges[i], edges[i + 1]);
            }
        }

        public void AddEdges(IEnumerable<Tuple<T, T>> edges)
        {
            foreach (var edge in edges) { AddEdge(edge.Item1, edge.Item2); }
        }

        public bool RemoveEdge(T from, T to)
        {
            return DGraph.RemoveEdge(from, to) && DGraph.RemoveEdge(to, from);
        }

        public void RemoveVertex(T v)
        {
            DGraph.RemoveVertex(v);
        }

        public IEnumerable<Tuple<T, T>> Edges
        {
            get
            {
                return DGraph.Edges;
            }
        }

        public override string ToString()
        {
            var ret = new StringBuilder();
            ret.AppendFormat("UndirectedGraph<{0}>: ", typeof(T).Name);
            var ourEdges = new HashSet<Tuple<T, T>>();
            foreach (Tuple<T, T> edge in Edges)
            {
                if (ourEdges.Contains(Tuple.Create(edge.Item2, edge.Item1)))
                {
                    continue;
                }
                ourEdges.Add(edge);
            }
            foreach (Tuple<T, T> edge in ourEdges)
            {
                ret.AppendFormat("{0}-{1} ", edge.Item1, edge.Item2);
            }
            return ret.ToString();
        }

        bool IGraphEdges<T>.IsNeighbour(T vertex, T possibleNeighbour)
        {
            return ((IGraphEdges<T>)DGraph).IsNeighbour(vertex, possibleNeighbour);
        }

        IEnumerable<T> IGraphEdges<T>.GetNeighbours(T vertex)
        {
            return ((IGraphEdges<T>)DGraph).GetNeighbours(vertex);
        }

        IEnumerable<Tuple<T, T>> IGraphEdges<T>.AsDirectedEdges(T from, T to)
        {
            yield return Tuple.Create(from, to);
            yield return Tuple.Create(to, from);
        }
    }

    // Path finding class
    public static class GraphPathFinding
    {
        // Using generics, so one==two not allowed.  See Skeet, "C# in Depth" and MSDN docs.
        private static bool Eq<T>(T one, T two)
        {
            return EqualityComparer<T>.Default.Equals(one, two);
        }

        // Useful extension methods
        static public void Add<T>(this List<T> list, IEnumerable<T> toAdd)
        {
            foreach (T x in toAdd) { list.Add(x); }
        }
        static public void Push<T>(this Stack<T> stack, IEnumerable<T> toPush)
        {
            foreach (T x in toPush) { stack.Push(x); }
        }
        static public void Remove<T>(this HashSet<T> set, IEnumerable<T> toRemove)
        {
            foreach (T x in toRemove) { set.Remove(x); }
        }

        // Perform a depth-first search from `startVertex`
        static public IEnumerable<T> DepthFirstSearch<T>(this IGraphEdges<T> graph, T startVertex)
        {
            var vertices = new HashSet<T>(); // Vertices we've visited already or are on the stack.
            var stack = new Stack<T>();
            stack.Push(startVertex);
            vertices.Add(startVertex);
            while (stack.Count() > 0)
            {
                T currentVertex = stack.Pop();
                yield return currentVertex;
                foreach (T v in graph.GetNeighbours(currentVertex))
                {
                    if (!vertices.Contains(v))
                    {
                        stack.Push(v); vertices.Add(v);
                    }
                }
            }
        }

        // Depth first search for path from `from` and to `to`.
        // Returns an empty List if no path.
        public static List<T> FindPath<T>(this IGraphEdges<T> graph, T startVertex, T to)
        {
            if (Eq(startVertex, to))
            {
                var singlePath = new List<T>();
                singlePath.Add(startVertex);
                return singlePath;
            }
            // Dictionary to store vertices we can reach and the vertex we visited before.
            var lookup = new Dictionary<T, T>();
            // Stack of vertices to explore next
            var toVisit = new Stack<Tuple<T, T>>();
            var willVisit = new HashSet<T>();
            foreach (T vertex in graph.GetNeighbours(startVertex))
            {
                toVisit.Push(Tuple.Create(vertex, startVertex));
                willVisit.Add(vertex);
            }
            while (toVisit.Count() > 0)
            {
                Tuple<T, T> PairWhereFrom = toVisit.Pop();
                T vertex = PairWhereFrom.Item1;
                T vertexFrom = PairWhereFrom.Item2;
                lookup[vertex] = vertexFrom;
                willVisit.Remove(vertex);
                if (Eq(vertex, to))
                {
                    break; // Found the end point, so can end
                }
                foreach (T v in graph.GetNeighbours(vertex))
                {
                    if (!lookup.ContainsKey(v) && !willVisit.Contains(v))
                    {
                        toVisit.Push(Tuple.Create(v, vertex));
                        willVisit.Add(v);
                    }
                }
            }
            // Extract path from `to` to `startVertex`, working backwards
            var path = new List<T>();
            if (!lookup.ContainsKey(to))
            {
                return path;
            }
            var currentVertex = to;
            while (!Eq(currentVertex, startVertex))
            {
                path.Add(currentVertex);
                currentVertex = lookup[currentVertex];
            }
            path.Add(startVertex);
            path.Reverse();
            return path;
        }


        /** Find edge-disjoint paths
         *  Uses variant of Ford-Fulkerson algorithm.
         *  See http://matthewdaws.github.io/Paths.html **/

        // Actually does the work, and returns a Set of directed edges which form the paths
        private static HashSet<Tuple<T, T>> EdgeDisjointPaths<T>(this IGraphEdges<T> graph, T startVertex, T to)
        {
            // We store the current paths as simply a list of edges used.
            var currentPaths = new HashSet<Tuple<T, T>>();
            if (Eq(startVertex, to)) { return currentPaths; }
            var edges = new List<Tuple<T, T>>();
            foreach (T vertex in graph.DepthFirstSearch(startVertex))
            {
                edges.Add(from end in graph.GetNeighbours(vertex) select Tuple.Create(vertex, end));
            }
            // Now apply the FF algorithm
            // Rather than build a new residual graph each time, keep a copy and update
            var residual = new DirectedGraph<T>();
            residual.AddEdges(edges);
            while (true)
            {
                var newPath = residual.FindPath(startVertex, to);
                if (newPath.Count() == 0)
                {
                    return currentPaths; // End, so return number of paths found
                }
                // Now merge new paths into both residual graph and collection of used edges
                for (int index = 0; index < newPath.Count() - 1; ++index)
                {
                    var edge = Tuple.Create(newPath[index], newPath[index + 1]);
                    var revEdge = Tuple.Create(newPath[index + 1], newPath[index]);
                    if (currentPaths.Contains(revEdge))
                    {
                        currentPaths.Remove(revEdge);
                        foreach (var e in graph.AsDirectedEdges(edge.Item1, edge.Item2)) { residual.RemoveEdge(e.Item1, e.Item2); }
                        foreach (var e in graph.AsDirectedEdges(revEdge.Item1, revEdge.Item2)) { residual.AddEdge(e.Item1, e.Item2); }
                    }
                    else
                    {
                        currentPaths.Add(edge);
                        foreach (var e in graph.AsDirectedEdges(edge.Item1, edge.Item2)) { residual.RemoveEdge(e.Item1, e.Item2); }
                        residual.AddEdge(revEdge.Item1, revEdge.Item2);
                    }
                }
            }
        }

        // Really a test function; checks the passed set of edges forms a collection of loops.
        private static bool CheckUnionLoops<T>(HashSet<Tuple<T, T>> edges)
        {
            var ourEdges = new HashSet<Tuple<T, T>>(edges); // Take a copy to mutate
            while (ourEdges.Count() > 0)
            {
                var start = ourEdges.First().Item1;
                var currentVertex = start;
                do
                {
                    if (!ourEdges.Any(e => Eq(e.Item1, currentVertex)))
                    {
                        return false;
                    }
                    var edge = ourEdges.First(e => Eq(e.Item1, currentVertex));
                    ourEdges.Remove(edge);
                    currentVertex = edge.Item2;
                } while (!Eq(currentVertex, start));
            }
            return true;
        }

        // Pass in a list of directed edges which form paths from `startVertex` to `to`.
        //   Warning: Mutates `pathEdges`
        // Returns a list of paths (in form of vertices).
        private static List<List<T>> ConvertEdgesToPaths<T>(HashSet<Tuple<T, T>> pathEdges, T startVertex, T to)
        {
            var paths = new List<List<T>>();
            while (pathEdges.Count() > 0)
            {
                // Subtle issue: our algorithm can return self-contained loops!  So check...
                if (!pathEdges.Any(e => Eq(e.Item1, startVertex)))
                {
                    break;
                }
                var newPath = new List<T>();
                T currentVertex = startVertex;
                while (!Eq(to, currentVertex))
                {
                    newPath.Add(currentVertex);
                    var edge = pathEdges.First(e => Eq(e.Item1, currentVertex));
                    pathEdges.Remove(edge);
                    currentVertex = edge.Item2;
                }
                newPath.Add(currentVertex);
                paths.Add(newPath);
            }
            return paths;
        }

        // Returns the maximum number of edge-disjoint paths from `startVertex` to `to`, or 0 is no path.
        public static List<List<T>> FindEdgeDisjointPaths<T>(this IGraphEdges<T> graph, T startVertex, T to)
        {
            if (Eq(to, startVertex))
            {
                var paths = new List<List<T>>();
                paths.Add(new List<T>());
                paths[0].Add(startVertex);
                return paths;
            }
            HashSet<Tuple<T, T>> pathEdges = graph.EdgeDisjointPaths(startVertex, to);
            return ConvertEdgesToPaths(pathEdges, startVertex, to);
        }

        public static int CountEdgeDisjointPaths<T>(this IGraphEdges<T> graph, T startVertex, T to)
        {
            if (Eq(startVertex, to)) { return 1; }
            var pathEdges = graph.EdgeDisjointPaths(startVertex, to);
            return pathEdges.Where(edge => Eq(edge.Item1, startVertex)).Count();
        }

        /** Second implementation, using a direct implementation of the "residual graph" **/

        // Pass in a set of directed edges which form edge-disjoint paths from `startVertex` to end.
        // Yield returns pairs (vertex, parent) when walking the "residual" graph.
        //   Special case: (startVertex, default(T))
        public static IEnumerable<Tuple<T, T>> AccessibleVerticesEDP<T>(this IGraphEdges<T> graph, T startVertex, HashSet<Tuple<T, T>> pathEdges)
        {
            // Pairs (next, parent)
            var toVisit = new Stack<Tuple<T, T>>();
            toVisit.Push(Tuple.Create(startVertex, default(T)));
            var visited = new HashSet<T>();
            visited.Add(startVertex);
            while (toVisit.Count() > 0)
            {
                var vertexPair = toVisit.Pop();
                var vertex = vertexPair.Item1;
                yield return vertexPair;
                // Check neighbours; can't walk on current path
                foreach (var v in graph.GetNeighbours(vertex))
                {
                    var edge = Tuple.Create(vertex, v);
                    if (!visited.Contains(v) && !pathEdges.Contains(edge))
                    {
                        toVisit.Push(Tuple.Create(v, vertex));
                        visited.Add(v);
                    }
                }
                // In the _directed_ case need to also consider that we can walk "backwards" on pathEdges
                // so need to search.  This is slow...
                foreach (var edge in pathEdges)
                {
                    if ( Eq(vertex, edge.Item2) && !visited.Contains(edge.Item1) )
                    {
                        toVisit.Push(Tuple.Create(edge.Item1, vertex));
                        visited.Add(edge.Item1);
                    }
                }
            }
        }

        // Pass in a maximal set of edge-disjoint paths from `startVertex` to some end point
        // Returns a cut: a minimal list of (directed) edges to delete to disconnect `startVertex` from the end point.
        public static HashSet<Tuple<T, T>> FindCutEDP<T>(this IGraphEdges<T> graph, T startVertex, HashSet<Tuple<T, T>> pathEdges)
        {
            var accessible = new HashSet<T>(
                from pair in graph.AccessibleVerticesEDP(startVertex, pathEdges)
                select pair.Item1);
            return new HashSet<Tuple<T, T>>(
                from start in accessible
                from end in graph.GetNeighbours(start)
                where !accessible.Contains(end)
                select Tuple.Create(start, end));
        }

        // New implementation, using Enumerable from above (so doesn't directly form the "residual graph").
        private static HashSet<Tuple<T, T>> EdgeDisjointPaths1<T>(this IGraphEdges<T> graph, T startVertex, T to)
        {
            var currentPaths = new HashSet<Tuple<T, T>>();
            if (Eq(startVertex, to)) { return currentPaths; }
            while (true)
            {
                // lookup[vertex] = parent of vertex; so there is an edge lookup[vertex] -> vertex
                var lookup = new Dictionary<T, T>();
                bool foundTo = false;
                foreach (var vertexPair in graph.AccessibleVerticesEDP(startVertex, currentPaths))
                {
                    // Edge from parent -> vertex
                    var vertex = vertexPair.Item1;
                    var parent = vertexPair.Item2;
                    if (!Eq(vertex, startVertex)) { lookup[vertex] = parent; }
                    if (Eq(vertex, to)) { foundTo = true; break; }
                }
                if (!foundTo) { break; }
                T current = to;
                while (!Eq(startVertex, current))
                {
                    var edge = Tuple.Create(lookup[current], current);
                    var revEdge = Tuple.Create(current, lookup[current]);
                    current = lookup[current];
                    if (!currentPaths.Remove(revEdge))
                    {
                        currentPaths.Add(edge);
                    }
                }
            }
            return currentPaths;
        }

        public static List<List<T>> FindEdgeDisjointPaths1<T>(this IGraphEdges<T> graph, T startVertex, T to)
        {
            if (Eq(to, startVertex))
            {
                var paths = new List<List<T>>();
                paths.Add(new List<T>());
                paths[0].Add(startVertex);
                return paths;
            }
            HashSet<Tuple<T, T>> pathEdges = graph.EdgeDisjointPaths1(startVertex, to);
            return ConvertEdgesToPaths(pathEdges, startVertex, to);
        }

        public static int CountEdgeDisjointPaths1<T>(this IGraphEdges<T> graph, T startVertex, T to)
        {
            if (Eq(startVertex, to)) { return 1; }
            var pathEdges = graph.EdgeDisjointPaths1(startVertex, to);
            return pathEdges.Where(edge => Eq(edge.Item1, startVertex)).Count();
        }


        /** Finding vertex-disjoint paths
         * First version uses an auxiliary directed graph, and the edge-disjoint path finding from above. **/

        // Find maximal set of vertex disjoint paths: returns the set of edges used.
        public static HashSet<Tuple<T, T>> VertexDisjointPaths<T>(this IGraphEdges<T> graph, T startVertex, T to)
        {
            if (Eq(startVertex, to) || graph.GetNeighbours(startVertex).Contains(to))
            {
                return new HashSet<Tuple<T, T>>();
            }
            // So `startVertex` and `to` are not the same, and not neighbours
            // Build new directed graph; (t,0) is the "in" vertex for t, and (t,1) the "out" vertex.
            var transformed = new DirectedGraph<Tuple<T, int>>();
            // Make "vertex edges", except start/finish
            foreach (var v in graph.DepthFirstSearch(startVertex))
            {
                if (!Eq(startVertex, v) && !Eq(to, v))
                {
                    transformed.AddEdge(Tuple.Create(v, 0), Tuple.Create(v, 1));
                }
            }
            // Link them all up
            foreach (var vout in graph.DepthFirstSearch(startVertex))
            {
                foreach (var vin in graph.GetNeighbours(vout))
                {
                    transformed.AddEdge(Tuple.Create(vout, 1), Tuple.Create(vin, 0));
                }
            }
            var transUsedEdges = transformed.EdgeDisjointPaths(Tuple.Create(startVertex, 1), Tuple.Create(to, 0));

            // Check
            foreach (var edge in transUsedEdges)
            {
                if (Eq(edge.Item1.Item1, edge.Item2.Item1))
                {
                    if (edge.Item1.Item2 != 0 || edge.Item2.Item2 != 1)
                    {
                        throw new Exception(String.Format("Backwards edge: {0}", edge));
                    }
                }
            }

            return new HashSet<Tuple<T, T>>(
                from edge in transUsedEdges
                where !Eq(edge.Item1.Item1, edge.Item2.Item1)
                select Tuple.Create(edge.Item1.Item1, edge.Item2.Item1));
        }

        // Returns a list of paths which form vertex-disjoint paths
        public static List<List<T>> FindVertexDisjointPaths<T>(this IGraphEdges<T> graph, T startVertex, T to)
        {
            var allPaths = new List<List<T>>();
            if (Eq(startVertex, to))
            {
                allPaths.Add(new List<T>());
                allPaths[0].Add(to);
                return allPaths;
            }
            if (graph.IsNeighbour(startVertex, to))
            {
                allPaths.Add(new List<T>());
                allPaths[0].Add(startVertex);
                allPaths[0].Add(to);
                return allPaths;
            }
            var pathEdges = graph.VertexDisjointPaths(startVertex, to);
            return ConvertEdgesToPaths(pathEdges, startVertex, to);
        }

        public static int CountVertexDisjointPaths<T>(this IGraphEdges<T> graph, T startVertex, T to)
        {
            return graph.FindVertexDisjointPaths(startVertex, to).Count();
        }

        /** Finding vertex-disjoint paths
         * Second version implements the algorithm directly without building residual graphs etc. **/

        // Main algorithm for Vertex-Disjoint Path finding.
        // Call with `usedEdges` being a set of vertex-disjoint paths.
        // Yield Returns pairs (vertex, parent) where vertex is any `vertex` accessible from startVertex, and `parent`
        //   is the vertex before.  As a special case yields (startVertex, default(T)).
        // For variety, this use a breadth-first search.
        // The only reason to ever re-visit a vertex `a` is if:
        //   - Before we came along an edge `b`-->`a` which is not on a reversed path
        //   - Now we are coming `c`-->`a` which is on a reversed path
        //   - A better way would be to log when we've visited `a` in a "full" capacity.
        internal static IEnumerable<Tuple<T, T>> AccessibleVerticesVDP<T>(this IGraphEdges<T> graph, T startVertex, HashSet<Tuple<T, T>> usedEdges)
        {
            // All vertices on a path, except startVertex
            var verticesOnPaths = new Dictionary<T, bool>();
            var predOnPaths = new Dictionary<T, T>();
            foreach (var edge in usedEdges)
            {
                verticesOnPaths[edge.Item2] = false;
                predOnPaths[edge.Item2] = edge.Item1;
            }
            
            var toVisit = new Queue<Tuple<T, T>>();
            var visited = new HashSet<T>();
            toVisit.Enqueue(Tuple.Create(startVertex, default(T)));
            visited.Add(startVertex);
            while ( toVisit.Count() > 0 )
            {
                var vertexPair = toVisit.Dequeue();
                var vertex = vertexPair.Item1;
                var parent = vertexPair.Item2;
                yield return vertexPair;
                // Where can we go next?
                if ( verticesOnPaths.ContainsKey(vertex) )
                {
                    // On path; where can we go to following path backwards?  Allow us to revisit if
                    // haven't been to this vertex "from the path" before.
                    T next = predOnPaths[vertex];
                    if ( ( !Eq(next, startVertex) && verticesOnPaths[next] == false )
                        || !visited.Contains(next) )
                    {
                        toVisit.Enqueue(Tuple.Create(next, vertex));
                        visited.Add(next);
                        verticesOnPaths[next] = true; // Will now visit `next` from path, so don't do this again!
                    }
                    if ( !usedEdges.Contains(Tuple.Create(vertex, parent)) )
                    {
                        continue; // Didn't come from path, so no other options.
                    }
                }
                // So "normal": look at neighbours
                foreach (T nhbr in graph.GetNeighbours(vertex))
                {
                    if ( !visited.Contains(nhbr) && !usedEdges.Contains(Tuple.Create(vertex, nhbr)) )
                    {
                        toVisit.Enqueue( Tuple.Create(nhbr, vertex) );
                        visited.Add(nhbr);
                    }
                }
            }
        }
        
        // Uses our search above to find a maximal family of vertex disjoint paths.
        // If the path finding algorithm, it builds a dictionary of accessible vertices and a viable edge
        //   _to_ that vertex.  Once we find the `to` vertex we work backwards to find a new path.
        // Because of the "non-local" rules of path-finding in the "residual" graph, this gets complicated!
        // However, the _only_ complication is that if our vertex search algorithm returns an edge
        //   `parent`->`vertex` with `parent` on a path and `vertex` not, then _previously_ to this,
        //   it must have returned an edge `prev`->`parent` which is the reverse of a used edge.
        public static List<List<T>> FindVertexDisjointPaths1<T>(this IGraphEdges<T> graph, T startVertex, T to)
        {
            // Corner cases for `startVertex` and `to`
            var allPaths = new List<List<T>>();
            if (Eq(startVertex, to))
            {
                allPaths.Add(new List<T>());
                allPaths[0].Add(to);
                return allPaths;
            }
            if (graph.IsNeighbour(startVertex, to))
            {
                allPaths.Add(new List<T>());
                allPaths[0].Add(startVertex);
                allPaths[0].Add(to);
                return allPaths;
            }
            // Apply FF algorithm
            return graph.FindVertexDisjointPaths1(startVertex, to, new HashSet<Tuple<T, T>>());
        }

        // Variant which allows us to start with some existing paths: useful if e.g. the application
        // comes with some "obvious" paths we can start from.  This assumes that `startVertex` and `to`
        // are not equal or neighbours.
        public static List<List<T>> FindVertexDisjointPaths1<T>(this IGraphEdges<T> graph, T startVertex, T to, HashSet<Tuple<T, T>> edges)
        {
            var usedEdges = new HashSet<Tuple<T, T>>(edges);
            while (true)
            {
                // newPath[vertex] == predecessor of vertex; i.e. edge from newPath[vertex] to vertex
                var lookup = new Dictionary<T, T>();
                // Problem: It's possible to visit the same vertex twice (thanks to non-local walking rules)
                var backup = new Dictionary<T, T>();
                bool canReachTo = false;
                foreach (var vertexPair in graph.AccessibleVerticesVDP(startVertex, usedEdges))
                {
                    // Edge from vertexPair.Item2 to vertexPair.Item1
                    if (Eq(startVertex, vertexPair.Item1)) { continue; }
                    if ( lookup.ContainsKey(vertexPair.Item1) )
                    {
                        backup[vertexPair.Item1] = lookup[vertexPair.Item1];
                    }
                    lookup[vertexPair.Item1] = vertexPair.Item2;
                    if (Eq(to, vertexPair.Item1)) { canReachTo = true; break; }
                }
                if (!canReachTo) { break; }
                var vertex = to;
                while (!Eq(vertex, startVertex))
                {
                    var edge = Tuple.Create(lookup[vertex], vertex);
                    var revEdge = Tuple.Create(vertex, lookup[vertex]);
                    if (!usedEdges.Remove(revEdge))
                    {
                        usedEdges.Add(edge);
                    }
                    if (backup.ContainsKey(vertex))
                    {
                        T tmp = lookup[vertex];
                        lookup[vertex] = backup[vertex];
                        vertex = tmp;
                    }
                    else
                    {
                        vertex = lookup[vertex];
                    }
                }
            }
            // Assemble Paths
            return ConvertEdgesToPaths(usedEdges, startVertex, to);
        }


        // Call with `paths` being a family of paths from startVertex to some end point.  This family should
        // be vertex-disjoint and maximal.
        // Returns a cut.
        public static List<T> FindCutVDP<T>(this IGraphEdges<T> graph, T startVertex, List<List<T>> paths)
        {
            var usedEdges = new HashSet<Tuple<T, T>>();
            foreach (var path in paths)
            {
                for (int i = 0; i < path.Count() - 1; ++i)
                {
                    usedEdges.Add(Tuple.Create(path[i], path[i + 1]));
                }
            }
            var accessible = new HashSet<T>(from pair in graph.AccessibleVerticesVDP(startVertex, usedEdges) select pair.Item1);
            var cut = new HashSet<T>(
                from vertex in accessible
                from v in graph.GetNeighbours(vertex)
                where !accessible.Contains(v)
                select vertex);
            if (cut.Remove(startVertex))
            {
                foreach (var v in graph.GetNeighbours(startVertex))
                {
                    if (!accessible.Contains(v)) { cut.Add(v); }
                }
            }
            return new List<T>(cut);
        }
    }

}