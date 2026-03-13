from fastapi import APIRouter,Depends,HTTPException,status
from typing import List
from  sqlalchemy.orm import Session
from sqlalchemy import text
from db_connection import DbConnection
from models import response_model
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from utils import utility
db_conn=DbConnection()

router=APIRouter(
    prefix="/login",
    tags=["users"]
)

@router.post(
    '/',
    status_code=status.HTTP_200_OK
)

def user_login(
    user_schema:response_model.user,
    db:Session=Depends(db_conn.get_db)
):
    # check email frst
    user=db.execute(text("select * from user where email=:email"),
                          params={
                            "email":user_schema.email
                          }).mappings().first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No email found")
    if not utility.verify_password(user_schema.password,user.password):
            raise  HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="password is incorrect"
            )
    else:
            return {"login":"success"}

    
    