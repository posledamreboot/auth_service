import bcrypt

def get_password_hash(password: str) -> str:
    # Bcrypt требует байты; автоматически генерирует соль
    password_bytes = password.encode("utf-8")
    # Обрезаем до 72 байт — как требует bcrypt
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode("utf-8")  # храним как строку

def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_bytes = plain_password.encode("utf-8")
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
    hashed_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(password_bytes, hashed_bytes)