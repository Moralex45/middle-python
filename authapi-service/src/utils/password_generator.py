import secrets
import string


def generator_pw():
    """
        Генерация рандомного пароля для пользователя.
    """
    pwd = string.ascii_letters + string.digits + string.punctuation
    safe_random = secrets.SystemRandom()
    return ''.join(safe_random.choice(pwd) for _ in range(safe_random.randint(6, 12)))
