import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

n = int(input())  # Number of elements which make up the association table.
q = int(input())  # Number Q of file names to be analyzed.
liste_a_comparer = {}
for i in range(n):
    # ext: file extension
    # mt: MIME type.
    ext, mt = input().split()
    liste_a_comparer[ext.lower()] = mt

for i in range(q):
    fname = input().strip()  # One file name per line.
    parts = fname.split('.')
    
    if len(parts) > 1 and parts[-1]:  # Check that the last part isn't empty
        file_extension = parts[-1].lower()
    else:
        file_extension = ""  # No valid extension found
    
    if file_extension in liste_a_comparer:
        result = liste_a_comparer[file_extension]
    else:
        result = "UNKNOWN"
    print(result)