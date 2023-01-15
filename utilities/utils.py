
import secrets
import string


def generate_random_string(length: int, letters=string.ascii_uppercase + string.ascii_lowercase + string.digits + '_' + '-') -> str:
    return ''.join(secrets.choice(letters) for i in range(0, length))
