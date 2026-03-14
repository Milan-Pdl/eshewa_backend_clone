from fastapi import APIRouter,Depends,HTTPException,status
from typing import List
from  sqlalchemy.orm import Session
from sqlalchemy import text
from db_connection import DbConnection
from models import response_model,db_model
from utils import utility
import random
db_conn=DbConnection()

router=APIRouter(
    prefix="/users",
    tags=["users"]
)

# @router.get('/')
# def welcome() -> dict:
#     return {"status":"welcome to the club"}



@router.post(
    '/register',
    status_code=status.HTTP_201_CREATED,
    response_model=response_model.UserResponse
)

def register_user(
    userschema:response_model.user,
    db:Session=Depends(db_conn.get_db)
):
    # generating random account number
    account_number = random.randint(100000000000, 999999999999)
    print(userschema.password)
    print(type(userschema.password))
    hashed_pass=utility.hash_password(userschema.password)
    userschema.password=hashed_pass
    new_user=db_model.User(**userschema.model_dump(),account_number=account_number)
    db.add(new_user)
    db.commit()
    return new_user

@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=List[response_model.UserResponse]
    # hamro response ma yek vanada dhere record aauna sakxa tei vayara response model lai list vitra rakhako..
)

def get_user(
    db: Session = Depends(db_conn.get_db),
):
    sql = text("SELECT * FROM user")
    result = db.execute(sql).mappings().all()
    # raw sql chai tuple ma result aauxa ni ta tei vayara hami la mapping la map graxam

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No any user"
        )

    return result

