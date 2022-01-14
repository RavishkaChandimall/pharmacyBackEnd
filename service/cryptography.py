from passlib.hash import pbkdf2_sha256


class Cryptography:
    def encrypt(self, password):
        return pbkdf2_sha256.encrypt(password, rounds=12000, salt_size=32)

    def validate(self, password, enc_password):
        return pbkdf2_sha256.verify(password, enc_password)
