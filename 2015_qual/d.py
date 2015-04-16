# Ominous Omino
#
# I hope in jetlag I have this correct.  I think we can do a lot of preparation,
# and reduce this to almost a triviality.
#
# If X>=7 then Richard can always form an X-ominoe which forms a ring (an
#   example is given for X=7) and this disconnects the plane which Gabriel
#   cannot recover from.
#   E.g.  Richard plays:  ###   The Gabriel cannot fill the middle part
#                         # #
#                         ##
#
# Clearly RC must be a multiple of X for Gabriel to have a hope
#
# Richard can form shapes of size X-by-1 then (X-1)-by-2 then (X-2)-by-3 and so
#   forth.  So we need a space of size X-by-ceil(X/2) in R-by-C or else Richard
#   can play such a shape which cannot fit.
# Need:  max(R,C) >= X and min(R,C) >= (X+1)//2
#
# X==1 : Trivial
#
# X==2 : R or C must be even and then Gabriel can win
#
# X==3 : R or C must be a multiple of 3 (as 3 is prime) and min(R,C) >= 2, and
#   then Gabriel can win.
#
# X==4 : max(R,C)>=4 and min(R,C) >= 2.  Richard can win if he plays:   ###
#                                                                        #
#   and e.g. R=2, C=4: then Gabriel can only play: ###-
#                                                  -#--  which cannot be a win.
#   If e.g. R=2 and C is arbitrary (and even) then this piece will always leave
#   an odd number of spaces on either side.
#   If min(R,C) >= 3 then Gabriel wins.  Perhaps this needs a touch of
#   justification, as Richard could play   ##  for 3 by 4
#                                         ##
#   but Gabriel can win as:  1123
#                            1223
#                            1233   with the 2s being Richard's piece.
#
# X==5 : min(R,C) >= 3 and one of R, C is a multiple of 5.  Again, Richard can
#   win if R=3 < C, as he can play:   ##  or rotated:  ##
#                                    ##                 ##  (same as reflected)
#                                    #                   #
#   Then on one side we always have 3x+1 spaces, and this is a multiple of 5
#   only for x=3 (10), x=8 (25) and so on.  So C needs to be a multiple of 5,
#   and >=6 for Gabriel to win.
#   The other choices of size 3-by-3 leave 2 spaces on either side, which means
#   Gabriel can position correctly.
#   We should also worry about the R=4 < C case, with the piece  ##
#                                                                 ###
#   But this is okay.
#
# X==6 : min(R,C) >= 3.  Again, problems if R=3 < C as then Richard can play:
#           #
#          ####    and then on the left (in this orientation) we always have
#           #            3x + 2 spaces which is never a multiple of 6.
#   If min(R,C)>=4 then all is okay (as max(R,C)>=6 by other constraints).
#
# If Richard cannot force a disconnection of the rectangle, then a simple "flood
#   fill" algorithm allows Gabriel to win.  With X<=6, the only shapes we can
#   make are sufficiently simple that this cannot fail.




import sys
num_cases = int(input())

for case in range(1, num_cases+1):
    X, R, C = [int(x) for x in input().split()]
    if ( X >= 7 or
        ( (R * C) % X != 0 ) or
        ( max(R,C) < X ) or ( min(R,C) < (X+1)//2 ) ):
        output = "RICHARD"
    else:
        # Make R <= C
        if R > C:
            R, C = C, R
        # Special cases as above
        if X == 4 and R == 2:
            output = "RICHARD"
        elif X == 5 and R == 3 and C == 5:
            output = "RICHARD"
        elif X == 6 and R == 3:
            output = "RICHARD"
        else:
            output = "GABRIEL"

    print("Case #{}: {}".format(case, output))
