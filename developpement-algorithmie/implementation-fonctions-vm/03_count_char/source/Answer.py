# Use print("Debug messages...") to debug your solution.

from typing import Optional, Dict

def count_char(txt: Optional[str]) -> Dict[str, int]:
    result = {}
    for letter in txt:
        if letter not in result:
            result[letter] = 0
        result[letter] += 1    
    return result
