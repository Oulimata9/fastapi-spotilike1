from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional
from decouple import config
# ...

# Clé secrète pour signer le token (à remplacer par votre propre clé secrète)
secret_key = config("secret")
Algo = config("ALGORITHM")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=Algo)
    return encoded_jwt
