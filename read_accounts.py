def read_credentials_file(file_path):
    credentials = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.replace('email: ', '')
            line = line.replace('password: ', '')
            line = line.strip()

            [email, password] = line.split(' ')

            credentials.append([email, password])
    return credentials
