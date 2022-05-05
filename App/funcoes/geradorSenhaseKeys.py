def getKey():
    import string
    import random
    random_str = string.ascii_letters + string.digits + string.ascii_uppercase
    return ''.join(random.choice(random_str) for i in range(12))