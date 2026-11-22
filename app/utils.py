from datetime import datetime, timezone, timedelta
from app.config import Securitysettings as st
import jwt

def generate_access_token(data: dict,expiry:timedelta = timedelta(days=1)):
    return jwt.encode(
            payload = {
                **data,
                "exp":datetime.now(timezone.utc)+expiry
            },
            algorithm=st.JWT_ALGORITHM,
            key = st.JWT_SECRET
        )

def decode_access_token(token:str)->dict:
    try:
        return jwt.decode(
                jwt=token,
                algorithms=[st.JWT_ALGORITHM],
                key=st.JWT_SECRET
            )
    except jwt.PyJWTError:
        return None