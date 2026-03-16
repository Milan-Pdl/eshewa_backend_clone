import  jwt
from jwt import PyJWTError
import json
from datetime import datetime,timedelta,timezone
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from db_connection import DbConnection
from fastapi import Depends,HTTPException,status
from models import db_model
db_conn=DbConnection()
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth_schema=OAuth2PasswordBearer(tokenUrl="login")
# yesla chai logins vanna endpoint ma gayara jwt token payinxa vanara vanxa


def get_sercret_key():
    with open("D:\project\eshewa_backend\config.json",'r') as f:
        key=json.loads(f.read())["SECRET_KEY"]
        return key

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, get_sercret_key(), algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token:str,credentials_exceptions:Exception):
    try:
        payload=jwt.decode(token,get_sercret_key(),[ALGORITHM])
        id=payload.get("id") 
        if id is None:
            raise credentials_exceptions
    except PyJWTError:
        raise credentials_exceptions
    return id
    

def get_user(token:str=Depends(oauth_schema),db:Session=Depends(db_conn.get_db)):
    credential_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                       detail="couldnot validate credentials",
                                       headers={"WWW-Authenticate":"bearer"})
    user_id=verify_token(token,credential_exception)
    user=db.query(db_model.User).filter(db_model.User.id ==user_id).first()
    return user





