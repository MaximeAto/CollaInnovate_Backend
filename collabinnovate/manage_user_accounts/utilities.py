import random


def generate_ping_code():
    return '{:05d}'.format(random.randint(0, 99999))