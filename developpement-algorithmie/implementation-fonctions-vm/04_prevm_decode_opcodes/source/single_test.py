# To use the candidate's code, import the module Answer
import Answer

# Use the print(...) function to output data.

# Only the lines of code between DISPLAY_BEGIN and DISPLAY_END
# will be shown to the final user.
# ##DISPLAY_BEGIN##
buf = b"\xf0\xf0"
e = Answer.decode_opcodes(buf)
assert e == [(Answer.TypeOfChunk.DATANULL, None), (Answer.TypeOfChunk.DATANULL, None)]
print(f"buffer décodé: {e}")

buf = b"\xf1\x42"
e = Answer.decode_opcodes(buf)
assert e == [(Answer.TypeOfChunk.DATAOPCODE, b'B')]
print(f"buffer décodé: {e}")

buf = b"\xf2\x00\x01\x02\x03"
e = Answer.decode_opcodes(buf)
assert e == [(Answer.TypeOfChunk.DATAINT, 66051)]
print(f"buffer décodé: {e}")

buf = b"\xf3\x04toto"
e = Answer.decode_opcodes(buf)
assert e == [(Answer.TypeOfChunk.DATASTR, 'toto')]
print(f"buffer décodé: {e}")

buf = b"\xf1\xcc\xf2\x00\x00\x0A\x28\xf3\x14\x43\x27\x65\x73\x74\x20\x63\x6F\x6F\x6C\x20\x6C\x65\x20\x70\x79\x74\x68\x6F\x6E\xf1\xff"
e = Answer.decode_opcodes(buf)
print(f"buffer décodé: {e}")
# ##DISPLAY_END##

