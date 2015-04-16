class Quat:
    rows = {"1":0, "i":1, "j":2, "k":3}
    reverserows = ["1", "i", "j", "k"]
    table = [ ["1", "i", "j", "k"],
             ["i", "-1", "k", "-j"],
             ["j", "-k", "-1", "i"],
             ["k", "j", "-i", "-1"] ]

    def __init__(self, val):
        if val[0] == "-":
            self.sign = -1
            self.val = Quat.rows[val[1]]
        else:
            self.sign = 1
            self.val = Quat.rows[val[0]]
        
    def __repr__(self):
        return "Quat("+str(self)+")"
    
    def __str__(self):
        s = ""
        if self.sign == -1:
            s += "-"
        return s + Quat.reverserows[self.val]
        
    def __eq__(self, other):
        return self.val == other.val and self.sign == other.sign
    
    def __mul__(self, other):
        val = Quat(Quat.table[self.val][other.val])
        val.sign *= self.sign * other.sign
        return val

    def __pow__(self, n):
        r = Quat("1")
        for _ in range(n % 4):
            r *= self
        return r

def choose_i(string):
    """Returns an iterable of integers n where string[:n] == i in the quaterion group."""
    prefix = Quat("1")
    for index, x in enumerate(string):
        prefix *= Quat(x)
        if prefix == Quat("i"):
            yield index+1

def choose_j(string):
    choices = []
    prefix = Quat("1")
    for index, x in enumerate(string):
        prefix *= Quat(x)
        if prefix == Quat("j"):
            yield index+1
            
def collapse(string):
    prefix = Quat("1")
    for x in string:
        prefix *= Quat(x)
    return prefix

import sys
num_cases = int(input())

for case in range(1, num_cases+1):
    length, repeat = [int(x) for x in input().split()]
    string = input()

    repeat = min(repeat, 12 + repeat % 4)
    string = string * repeat
    if collapse(string) != Quat("-1"):
        output = "NO"
    else:
        flag = False
        for istart in choose_i(string):
            substring = string[istart:]
            for jstart in choose_j(substring):
                if collapse(substring[jstart:]) == Quat("k"):
                    #print(istart, jstart)
                    flag = True
                    break
            if flag:
                break
        if flag:
            output = "YES"
        else:
            output = "NO"

    print("Case #{}: {}".format(case, output))
    print(case, num_cases, file=sys.stderr)
