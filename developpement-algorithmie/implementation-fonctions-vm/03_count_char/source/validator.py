# Add functions to this file, one for each method defined in 
# the Validators declared at the bottom of the page.

# Use assert (condition) to validate/unvalidate the candidate's answer which is
# in the Answer module
import Answer

from typing import Optional, Dict

def count_char(txt: Optional[str]) -> Dict[str, int]:
    if txt is None or not len(txt):
        return None
    d = {}
    for c in txt:
        if c not in d:
            d[c] = 1
        else:
            d[c] += 1
    return d

# basic validator
def validate():
    txt = "ceci est un test"
    res = count_char(txt)
    assert(Answer.count_char(txt) == res)

# validates that the code works for negative integers too
def emptyword():
    txt = ""
    assert(Answer.count_char(txt) is None)

# validates that the candidate's code works with one element (reliability)
def noneparam():
    assert(Answer.count_char(None) is None)
