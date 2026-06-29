# Use print("Debug messages...") to debug your solution.

from typing import List, Optional, Any

def make_pair(ls1: Optional[List[Any]], ls2: Optional[List[Any]]):
    result = []
    #Vérifier si les deux listes sont vides, donc opération impossible
    if (ls1 is None or len(ls1) == 0) and (ls2 is None or len(ls2) == 0):
        return ["None"]
    
    #Si la liste 2 est plus longue que la 1, on inverse les deux listes
    if len(ls2) > len(ls1):
        ls1, ls2 = ls2, ls1
    ls2 += [None] * (len(ls1) - len(ls2))
    
    #Création de la liste de tuples
    for i in range(len(ls1)):
        pair = (ls1[i], ls2[i])
        result.append(pair)
        
    return result
