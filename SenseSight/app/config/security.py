from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

import os
from dotenv import load_dotenv

pwd_crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth = OAuth2PasswordBearer(tokenUrl="auth/login")

ALGORITHM = os.getenv("ALGORITHM")
SECRET_KEY = os.getenv("SECRET_KEY")
REFRESH_SECRET_KEY = os.getenv("REFRESH_SECRET_KEY")
ACCESS_EXPIRY = os.getenv("ACCESS_EXPIRY")
REFRESH_EXPIRY = os.getenv("REFRESH_EXPIRY")
