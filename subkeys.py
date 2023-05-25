from table_perms_shifts import *
key = "0111101100111010101110110101010101100111011010010101010101111110"

# Functie pentru aplicarea permutarea initiala a cheii


def initial_permutation(key):
    permuted_key = ""
    for index in IP_TABLE:
        permuted_key += key[int(index) - 1]
    return permuted_key

# Functie pentru aplicarea permutarii inverse


def inverse_permutation(block):
    output_block = ""
    for index in IP_INVERSE_TABLE:
        output_block += block[int(index) - 1]
    return output_block

# Functie pentru rotiatia la stanga a jumatatilor cheii


def left_circular_shift(key, num_shifts):
    shifted_key = key[num_shifts:] + key[:num_shifts]
    return shifted_key

# Funcție pentru generarea sub-cheilor


def generate_subkeys(key):
    # Aplicam permutarea initiala cheii folosind tabela aferenta
    permuted_key = initial_permutation(key)

    # Impartim cheia permutata in doua jumatati pentru a
    # putea aplica rotatia circulara la stanga
    left_half = permuted_key[:28]
    right_half = permuted_key[28:]

    subkeys = []

    for round_num in range(16):
        # Realizam rotatia circulara folosind tabela NUM_SHIFTS
        left_half = left_circular_shift(left_half, NUM_SHIFTS[round_num])
        right_half = left_circular_shift(right_half, NUM_SHIFTS[round_num])

        # Aducem impreuna cele doua jumatati rotate
        combined_key = left_half + right_half

        # Creeam cheia aplicand din nou permutarea initiala
        subkey = initial_permutation(combined_key)

        # Adăugăm sub-cheia generată în listă
        subkeys.append(subkey)

    return subkeys

# Functia care returneaza cheile. O vom folosi in 'main.py'


def get_subkeys():
    return generate_subkeys(key)
