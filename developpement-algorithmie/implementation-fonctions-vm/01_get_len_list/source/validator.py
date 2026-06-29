# Add functions to this file, one for each method defined in 
# the Validators declared at the bottom of the page.

# Use assert (condition) to validate/unvalidate the candidate's answer which is
# in the Answer module
import Answer
from typing import List

def get_len_list(s: List[str]):
    return list(map(lambda _: len(_) if type(_) is str else 0, s))

# basic validator
def validate():
    test = ["ceci", "est", "une", "simple", "phrase"]
    res = get_len_list(test)
    assert(Answer.get_len_list(test) == res)

def oneword():
    test = ["helloword"]
    res = get_len_list(test)
    assert(Answer.get_len_list(test) == res)

def emptyword():
    test = ["hello", "", "world"]
    res = get_len_list(test)
    assert(Answer.get_len_list(test) == res)
