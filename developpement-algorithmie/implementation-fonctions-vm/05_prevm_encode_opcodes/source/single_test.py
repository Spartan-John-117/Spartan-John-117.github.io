# To use the candidate's code, import the module Answer
import Answer
from Answer import TypeOfChunk

# Use the print(...) function to output data.

# Only the lines of code between DISPLAY_BEGIN and DISPLAY_END
# will be shown to the final user.
# ##DISPLAY_BEGIN##
ls = [(TypeOfChunk.DATANULL, None)]
e = Answer.encode_opcodes(ls)
assert e == b'\xf0'
print(f"buffer encodé: {e}")
ls = [(TypeOfChunk.DATAOPCODE, b'U')]
e = Answer.encode_opcodes(ls)
assert e == b'\xf1U'
print(f"buffer encodé: {e}")
ls = [(TypeOfChunk.DATAINT, [SUPPRIME_2600])]
e = Answer.encode_opcodes(ls)
assert e == b'\xf2\x00\x00\n('
print(f"buffer encodé: {e}")
ls = [(TypeOfChunk.DATASTR, "attention! \u2620")]
print(ls[0][1])
e = Answer.encode_opcodes(ls)
assert e == b'\xf3\x0eattention! \xe2\x98\xa0'
print(f"buffer encodé: {e}")
ls = [(TypeOfChunk.DATAOPCODE, b'\xCC'), (TypeOfChunk.DATAINT, [SUPPRIME_2600]),
        (TypeOfChunk.DATASTR, "C'est cool le python"), (TypeOfChunk.DATAOPCODE, b'\xFF')]
e = Answer.encode_opcodes(ls)
assert e == b"\xf1\xcc\xf2\x00\x00\n(\xf3\x14C'est cool le python\xf1\xff"
print(f"buffer encodé: {e}")
# ##DISPLAY_END##

