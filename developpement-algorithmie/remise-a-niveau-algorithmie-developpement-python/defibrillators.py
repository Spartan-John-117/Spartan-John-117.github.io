import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

def distance(defib_lon, lon, defib_lat, lat):
    x = (defib_lon - lon) * math.cos((defib_lat + lat)/2)
    y = (lat - defib_lat)
    d = (math.sqrt(x**2 + y**2) * 6371)
    return d



lon = float(input().replace(",", "."))
lat = float(input().replace(",", "."))
n = int(input())
distance_min = math.inf
for i in range(n):
    defib = input().replace(",", ".").split(";")
    defib_nom = defib[1]
    defib_lon = float(defib[4])
    defib_lat = float(defib[5])
    distance_defib = distance(defib_lon, lon, defib_lat, lat)
    if distance_defib < distance_min:
        distance_min = distance_defib
        nom = defib_nom
    

# Write an answer using print
# To debug: print("Debug messages...", file=sys.stderr, flush=True)

print(nom)
