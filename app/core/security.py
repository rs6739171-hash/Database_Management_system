from fastapi.security import OAuth2PasswordBearer

auth2_scheme = oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/seller/login")