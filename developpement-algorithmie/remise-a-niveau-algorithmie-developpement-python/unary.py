import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

def message_to_binary(message):
    binary_message = ''.join(format(ord(char), '07b') for char in message)
    return binary_message

def encode_binary(binary):
    encoded_message = []
    i = 0
    while i < len(binary):
        bit = binary[i]
        count = 0
        while i < len(binary) and binary[i] == bit:
            count += 1
            i += 1
        
        if bit == '1':
            encoded_message.append(f'0 {"0" * count}')
        else:
            encoded_message.append(f'00 {"0" * count}')
    
    return ' '.join(encoded_message)

def encode_message(message):
    binary_message = message_to_binary(message)
    return encode_binary(binary_message)

message = input()
encoded = encode_message(message)
print(encoded)
