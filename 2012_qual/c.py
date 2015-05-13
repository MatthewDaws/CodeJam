class CountRecycle:
    def __init__(self, A, B):
        self.A, self.B = A, B
        self.length = 1
        self.pow10 = 1
        x = A
        while x >= 10:
            x //= 10
            self.pow10 *= 10
            self.length += 1
    
    def rotate(self, n):
        m = n
        for i in range(self.length - 1):
            m = (m // 10) + self.pow10 * (m % 10)
            if n < m and m <= self.B:
                yield m

    def countn(self, n):
        return len( set( self.rotate(n) ) )

    def count(self):
        return sum( self.countn(n) for n in range(A, B) )

num_cases = int(input())

for case in range(1, 1 + num_cases):
    A, B = [int(x) for x in input().split()]
    print("Case #{}: {}".format(case, CountRecycle(A, B).count()))
