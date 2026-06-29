import sys
import math

def closest(liste, K):
    return liste[min(
        range(len(liste)),
        key=lambda i: (abs(liste[i] - K), liste[i] < 0))]

n = int(input())

if n == 0:
    print(0)
else:
    temp_list = []

    for i in input().split():
        t = int(i)
        temp_list.append(t)

    temp_list.sort()

    min_temp = closest(temp_list, 0)

    print(min_temp)