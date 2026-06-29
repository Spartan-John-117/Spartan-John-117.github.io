# To use the candidate's code, import the module Answer
import Answer

# Use the print(...) function to output data.

# Only the lines of code between DISPLAY_BEGIN and DISPLAY_END
# will be shown to the final user.
# ##DISPLAY_BEGIN##
test1 = Answer.make_pair([7, 17, 13, 19, 5], ["riri", "fifi", "loulou"])
print(test1)
print("test:", test1 == [(7, 'riri'), (17, 'fifi'),
            (13, 'loulou'), (19, None), (5, None)]
            )
# ##DISPLAY_END##
