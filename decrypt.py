from subkeys import get_subkeys, inverse_permutation, initial_permutation
from table_expansion import EXPANSION_TABLE
from table_substitutions import S_BOXES
from table_perms_shifts import IP_TABLE, IP_INVERSE_TABLE, PERMUTATION_TABLE
from utils import binary_to_hex, hex_to_binary, xor, permutation


def decrypt(ciphertext, subkeys):
    # Transformam textul criptat in cod binar
    ciphertext_binary = hex_to_binary(ciphertext)
    plaintext = ""

    # Parcurgem bitii
    for i in range(0, len(ciphertext_binary), 64):
        block = ciphertext_binary[i:i + 64]

        # Ne asiguram ca are o lungime de 64 de biti
        if len(block) < 64:
            block += '0' * (64 - len(block))

        # Facem permutarea initiala
        block = initial_permutation(block)

        # Impartim blocurile in 2 jumatati
        left_half = block[:32]
        right_half = block[32:]

        for j in range(15, -1, -1):
            # Marim partea dreapta la 48 de biti
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
        plaintext_block = inverse_permutation(combined_block)

        # Pentru ca am avut probleme la crearea algoritmului, am inlocuit
        # caracterele care nu sunt in tabelul ASCII cu semnul intrebarii.
        plaintext += "".join(
            chr(int(plaintext_block[i:i + 8], 2)) if 32 <= int(
                plaintext_block[i:i + 8], 2) <= 126 else "?"
            for i in range(0, len(plaintext_block), 8)
        )

    # Scoatem paddingul din text
    plaintext = plaintext.rstrip("?")

    return plaintext
