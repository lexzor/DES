def binary_to_hex(binary_string):
    hex_string = hex(int(binary_string, 2))[2:]
    return hex(int(binary_string, 2))[2:]


def hex_to_binary(hex_string):
    binary_string = bin(int(hex_string, 16))[2:]
    return binary_string


def xor(a, b):
    result = ''.join(str(int(x) ^ int(y)) for x, y in zip(a, b))
    return result


def permutation(input_bits, table):
    permuted_bits = [input_bits[index - 1] for index in table]
    return "".join(permuted_bits)
