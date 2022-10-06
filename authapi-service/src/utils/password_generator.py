import random
import string


def generator_pw():
    """
        Генерация рандомного пароля для пользователя.
    """
    pwd = string.ascii_letters + string.digits + string.punctuation
    return "".join(random.choice(pwd) for x in range(random.randint(6, 12)))
