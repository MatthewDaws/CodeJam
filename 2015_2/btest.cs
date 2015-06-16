using System;
using System.Diagnostics;
using System.Collections.Generic;
using System.Linq;

// Class to store points in the upper half plane.  Our interest is in the unusual ordering.
struct MyStruct : IComparable<MyStruct>
{
    public int State;
    public MyStruct(int s) { State = s; }
    public int CompareTo(MyStruct rhs)
    {
        // 10 is the "min" state.  Otherwise order as usual
        if (State == 10) { return -1; }
        /*if (State == 10)
        {
            if (rhs.State == 10) { return 0; }
            return -1;
        }*/
        if (rhs.State == 10) { return 1; }
        return this.State - rhs.State;
    }
    public override string ToString()
    {
        return String.Format("MyStruct({0})", State);
    }
}

class Program
{
    static int Main()
    {
        var list = new List<MyStruct>();
        var rnd = new Random();
        for (int i = 0; i < 20; ++i)
        {
            int x = rnd.Next(15);
            if (x >= 10) { ++x;  }
            list.Add(new MyStruct(x));
        }
        list.Add(new MyStruct(10));
        //list.Sort();
        list = list.OrderBy(item => item).ToList();
        
        Console.WriteLine("list:");
        foreach (var x in list) { Console.WriteLine(x); }

        for (int i = 1; i < list.Count(); ++i)
        {
            Console.Write("{0} ", list[i].CompareTo(list[i - 1]));
        }

        return 0;
    }
}
