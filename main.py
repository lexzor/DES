from encrypt import encrypt as e
from decrypt import decrypt as d
from subkeys import get_subkeys as gs
from read_accounts import read_credentials_file as rf

subkeys = gs()
accounts = rf('accounts.txt')

output = []

for [email, password] in accounts:
    encrypted_email = e(email, subkeys)
    decrypted_email = d(encrypted_email, subkeys)

    encrypted_password = e(password, subkeys)
    decrypted_password = d(encrypted_password, subkeys)

    result_email = ''
    result_password = ''

    if email == decrypted_email:
        result_email = 'success'
    else:
        result_email = 'failed'

    if password == decrypted_password:
        result_password = 'success'
    else:
        result_password = 'failed'

    obj = {
        'result_em': result_email,
        'result_pw': result_password,
        'initial_email': email,
        'encrypted_email': encrypted_email,
        'decrypted_email': decrypted_email,
        'initial_password': password,
        'encrypted_password': encrypted_password,
        'decrypted_password': decrypted_password
    }

    print(obj)
