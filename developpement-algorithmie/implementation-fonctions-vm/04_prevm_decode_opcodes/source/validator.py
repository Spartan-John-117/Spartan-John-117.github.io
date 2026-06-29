# Add functions to this file, one for each method defined in 
# the Validators declared at the bottom of the page.

# Use assert (condition) to validate/unvalidate the candidate's answer which is
# in the Answer module
import Answer

# basic validator
def validate():
    buf = b"\xf0\xf0"
    e = Answer.decode_opcodes(buf)
    assert(e == [(Answer.TypeOfChunk.DATANULL, None), (Answer.TypeOfChunk.DATANULL, None)])

def validateOpcode():
    buf = b"\xf1\x42"
    e = Answer.decode_opcodes(buf)
    assert(e == [(Answer.TypeOfChunk.DATAOPCODE, b'B')])

def validateInt():
    buf = b"\xf2\x00\x01\x02\x03"
    e = Answer.decode_opcodes(buf)
    assert(e == [(Answer.TypeOfChunk.DATAINT, 66051)])

def validateStr():
    buf = b"\xf3\x04toto"
    e = Answer.decode_opcodes(buf)
    assert(e == [(Answer.TypeOfChunk.DATASTR, 'toto')])

def validateFinal():
    buf = b"\xf1\xcc\xf2\x00\x00\x0A\x28\xf3\x14\x43\x27\x65\x73\x74\x20\x63\x6F\x6F\x6C\x20\x6C\x65\x20\x70\x79\x74\x68\x6F\x6E\xf1\xff"
    e = Answer.decode_opcodes(buf)
    assert(e == [(Answer.TypeOfChunk.DATAOPCODE, b'\xcc'), (Answer.TypeOfChunk.DATAINT, [SUPPRIME_2600]), (Answer.TypeOfChunk.DATASTR, "C'est cool le python"), (Answer.TypeOfChunk.DATAOPCODE, b'\xff')])

