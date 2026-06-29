# Add functions to this file, one for each method defined in 
# the Validators declared at the bottom of the page.

# Use assert (condition) to validate/unvalidate the candidate's answer which is
# in the Answer module
import Answer
from Answer import TypeOfChunk

# basic validator
def validate():
    ls = [(TypeOfChunk.DATANULL, None)]
    e = Answer.encode_opcodes(ls)
    assert e == b'\xf0'

def validateOpcode():
    ls = [(TypeOfChunk.DATAOPCODE, b'U')]
    e = Answer.encode_opcodes(ls)
    assert e == b'\xf1U'

def validateInt():
    ls = [(TypeOfChunk.DATAINT, [SUPPRIME_2600])]
    e = Answer.encode_opcodes(ls)
    assert e == b'\xf2\x00\x00\n('

def validateStr():
    ls = [(TypeOfChunk.DATASTR, "attention! \uFE0F")]
    e = Answer.encode_opcodes(ls)
    assert e == b'\xf3\x0eattention! \xef\xb8\x8f'

def validateFinal():
    ls = [(TypeOfChunk.DATAOPCODE, b'\xCC'), (TypeOfChunk.DATAINT, [SUPPRIME_2600]),
            (TypeOfChunk.DATASTR, "C'est cool le python"), (TypeOfChunk.DATAOPCODE, b'\xFF')]
    e = Answer.encode_opcodes(ls)
    assert e == b"\xf1\xcc\xf2\x00\x00\n(\xf3\x14C'est cool le python\xf1\xff"
