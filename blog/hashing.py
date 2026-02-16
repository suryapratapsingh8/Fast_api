from passlib.context import CryptContext

# In this environment, passlib's bcrypt backend initialization is failing with:
# "ValueError: password cannot be longer than 72 bytes" (raised inside bcrypt during
# passlib's internal self-test). To keep things working, use a scheme that does NOT
# rely on the bcrypt backend.
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

class Hash:
    def bcrypt(password: str):
        return pwd_context.hash(password)