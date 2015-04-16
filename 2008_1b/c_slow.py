# Problem is that this is O(K^2) so K=10**6 is impossible.
def find_seq(K):
   n = 1
   seq = [K]
   while n < K:
      nextnum = K - n
      i = nextnum % (n+1)
      if i == 0:
         i = n + 1
      # i=1 at start, i=2 then pad etc.
      if i == 1:
         seq = [nextnum] + seq
      else:
         newseq = seq[-(i-1):]
         newseq.append(nextnum)
         newseq.extend( seq[:-(i-1)] )
         seq = newseq
      n += 1 # next loop
   return seq


num_cases = int(input())

for case in range(1, num_cases+1):
   K = int(input())   
   seq = find_seq(K)
   indices = [ int(x) for x in input().split() ]
   indices = indices[1:]
   print("Case #{}: {}".format(case, " ".join( str(seq[i-1]) for i in indices ) ) )