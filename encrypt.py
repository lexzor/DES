from subkeys import get_subkeys, initial_permutation, inverse_permutation
from table_expansion import EXPANSION_TABLE
from table_substitutions import S_BOXES
from table_perms_shifts import IP_TABLE, IP_INVERSE_TABLE, PERMUTATION_TABLE
from utils import binary_to_hex, hex_to_binary, xor, permutation


def encrypt(plaintext, subkeys):
    # Transformam textul in biti
    plaintext_binary = "".join(format(ord(c), "08b") for c in plaintext)

    # In cazul in care numarul de biti este mai mic decat 64, adaugam biti nuli (0)
    padding_length = 64 - len(plaintext_binary) % 64
    plaintext_binary += '0' * padding_length

    ciphertext = ""

    # Parcurgem blocul de 64 de biti
    for i in range(0, len(plaintext_binary), 64):
        block = plaintext_binary[i:i+64]

        # Facem permutarea initiala specifica algoritmului
        block = initial_permutation(block)

        # Impartim blocul de biti in 2 parti egale
        left_half = block[:32]
        right_half = block[32:]

        # Incepem Schema Feistel
        for j in range(16):
            # Crestem numarul de biti pentru partea dreapta la 48
            expanded_half = permutation(right_half, EXPANSION_TABLE)

            # Folosim o operatie de tip XOR pe biti cu subcheia specifica rundei
            xor_result = xor(expanded_half, subkeys[j])

            # Se aplica procesul de substitutie pentru biti
            substituted_half = ""

            for k in range(8):
                row = int(xor_result[k * 6] + xor_result[k * 6 + 5], 2)
                col = int(xor_result[k * 6 + 1:k * 6 + 5], 2)
                substituted_half += bin(S_BOXES[k][row][col])[2:].zfill(4)

            # Rearanjam bitii specific tabelei aferente
            permuted_half = permutation(substituted_half, PERMUTATION_TABLE)

            # Se face operatia XOR pentru jumatatea stanga care nu a fost schimbata si rezultatul
            # procesului de rearanjare a bitilor pentru partea dreapta
            xor_result = xor(left_half, permuted_half)

            # Schimbam intre ele cele 2 parti
            left_half = right_half
            right_half = xor_result

        # Combinam cele 2 parti care au fost rearanjate in Schema Feistel
        combined_block = right_half + left_half

        # Aplicam permutarea inversa
        ciphertext += inverse_permutation(combined_block)

    # Convertim si returnam textul sub forma de text hexadecimala
    return binary_to_hex(ciphertext)
