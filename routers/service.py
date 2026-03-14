from fastapi import APIRouter,Depends,HTTPException,status
from typing import List
import requests
from  sqlalchemy.orm import Session
from sqlalchemy import text
from db_connection import DbConnection
from models import response_model,db_model
from utils import utility
import random
db_conn=DbConnection()

router=APIRouter(
    prefix="/loadmoney",
    tags="bankservices"
)

def bank_user() ->list: 
    base_url="http://127.0.0.1:8000/bank/users"
    response=requests.get(base_url)
    return response.json()

def check_sender_email_status(user_email,password) ->bool:
    bank_users=bank_user()
    for users in bank_users:
        #  print(users)
         if users['Email']==user_email and users['password']==password:
             return users
         continue
print(check_sender_email_status("sujan.thapa@gmail.com"))
    

@router.post('/',status_code=status.HTTP_200_OK)
def load_in_eshewa(schema:response_model.LoadEshewa,db:Session=Depends()):
    sender_infomation=check_sender_email_status(schema.sender_email,schema.sender_pass)
    check_eshewa_id=db.execute(text("select email from user where email=:email"),
                               params={"email":schema.receiver_email}).mappings().first()
    
    if check_eshewa_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="no such user")

    db.execute(text("UPDATE user SET amount = amount + :amt WHERE email=:email"),
                         params={"amt":schema.amount,"email":schema.receiver_email})
    db.commit()

    



    


