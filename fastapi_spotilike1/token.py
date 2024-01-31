from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional

# ...

# Clé secrète pour signer le token (à remplacer par votre propre clé secrète)
secret = "ea504dfd74cdc3fbddcb4e67c73b6070"
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret, algorithm=ALGORITHM)
    return encoded_jwt
