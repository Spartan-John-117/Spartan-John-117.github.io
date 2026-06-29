# Add functions to this file, one for each method defined in 
# the Validators declared at the bottom of the page.

# Use assert (condition) to validate/unvalidate the candidate's answer which is
# in the Answer module
import Answer

from typing import List, Optional, Any

def make_pair(ls1: Optional[List[Any]], ls2: Optional[List[Any]]):
    if ls1 is None and ls2 is None:
        return None
    ls1 = ls1 if ls1 is not None else []
    ls2 = ls2 if ls2 is not None else []
    lr = []
    lm = max(len(ls1), len(ls2))
    for it in range(lm):
        if it < len(ls1):
            a = ls1[it]
        else:
            a = None
        if it < len(ls2):
            b = ls2[it]
        else:
            b = None
        lr.append((a, b))
    return lr

# basic validator
def validate():
    param = ([2, 4, 6, 8], [3, 6, 9])
    res = make_pair(*param)
    assert(Answer.make_pair(*param) == res)

# validates that the code works for negative integers too
def onelsnone():
    param = ([2, 4, 6, 8], None)
    res = make_pair(*param)
    assert(Answer.make_pair(*param) == res)

def oneothernone():
    param = (None, [2, 4, 6, 8])
    res = make_pair(*param)
    assert(Answer.make_pair(*param) == res)


# validates that the candidate's code works with one element (reliability)
def twolsnone():
    param = (None, None)
    assert(Answer.make_pair(*param) is None)
