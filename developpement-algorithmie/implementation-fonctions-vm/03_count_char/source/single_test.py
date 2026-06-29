# To use the candidate's code, import the module Answer
import Answer

# Use the print(...) function to output data.

# Only the lines of code between DISPLAY_BEGIN and DISPLAY_END
# will be shown to the final user.
# ##DISPLAY_BEGIN##
test1 = Answer.count_char("this is a test")
print(test1)
print("test:", test1 == {'t': 3, 'h': 1, 'i': 2, 's': 3, ' ': 3, 'a': 1, 'e': 1})
test2 = Answer.count_char("sushi cat and yakitori dog")
print(test2)
print("test:", test2 == {'s': 2, 'u': 1, 'h': 1, 'i': 3, ' ': 4,
                'c': 1, 'a': 3, 't': 2, 'n': 1, 'd': 2, 'y': 1, 'k': 1, 'o': 2,
                'r': 1, 'g': 1}
            )
# ##DISPLAY_END##

