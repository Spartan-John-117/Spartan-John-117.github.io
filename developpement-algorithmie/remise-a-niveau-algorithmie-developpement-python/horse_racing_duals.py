import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
difference_min = math.inf
n = int(input())
liste_puissance = [0] * n
for i in range(n):
    pi = int(input())
    liste_puissance[i] = pi
liste_puissance.sort()

for i in range(n):
    difference = liste_puissance[i] - liste_puissance[i -1]
    if difference < difference_min:
        difference_min = difference

# Write an answer using print
# To debug: print("Debug messages...", file=sys.stderr, flush=True)

print(difference_min)
