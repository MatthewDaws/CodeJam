import math

class Sqrt5modn:
    def __init__(self,a,b,n):
        self.n = n
        self.a, self.b = a % n, b % self.n
    
    def __add__(self, other):
        return Sqrt5modn((self.a + other.a) % self.n, (self.b + other.b) % self.n, self.n)
    
    def __mul__(self, other):
        return Sqrt5modn((self.a * other.a + self.b * other.b * 5) % self.n,
            (self.a * other.b + self.b * other.a) % self.n, self.n)
    
    def __pow__(self, n):
        ret = Sqrt5modn(1,0, self.n)
        power = Sqrt5modn(self.a, self.b, self.n)
        n2 = 1
        while n2 <= n:
            if n & n2 > 0:
                ret *= power
            n2 += n2
            power *= power
        return ret

    def __repr__(self):
        return "Sqrt5modn({}, {})".format(self.a, self.b)

num_cases = int(input())
for case in range(1, num_cases+1):
    x = Sqrt5modn(3,1,1000)
    n = int(input())
    x = x**n
    x = x.a
    print("Case #{}: {:03}".format(case, (x+x-1)%1000))