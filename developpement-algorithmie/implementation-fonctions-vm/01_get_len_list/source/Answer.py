from typing import List

def get_len_list(ls: List[str]):
    result = []
    for i in ls:
        counter = 0
        for word in i:
            counter += 1
        result.append(counter)
    return result
    
    

