import random
from hashlib import sha256

from common.settings import settings


class PasswordService:
    def __init__(self):
        self.chars = '+-*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'

    def new_password(self, len_password: int = 10) -> str:
        password = ""
        for _ in range(len_password):
            password += random.choice(self.chars)

        return password

    @staticmethod
    def hash_password(password: str) -> str:
        # do not change the hash function
        password = f'{password}{settings.salt_postfix}'
        hash_object = sha256()
        hash_object.update(password.encode())
        return hash_object.hexdigest()
