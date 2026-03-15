from fastapi import APIRouter,Depends,HTTPException,status
from typing import List
import requests
from  sqlalchemy.orm import Session
from sqlalchemy import text
from db_connection import DbConnection
from models import response_model,db_model
from utils import utility
from BankGateway.db_conn import DBConnection
import random
db_conn_bank=DBConnection()
db_conn_eshewa=DbConnection()

router=APIRouter(
    prefix="/loadmoney",
    tags=["bankservices"]
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
    
def check_receive_eshewa_id(receiver_email,db: Session) -> bool:
    """ this function checks if the receiver email is registerd in eshewa database"""
    return db.execute(text("select email from user where email=:email"),
                               params={"email":receiver_email}).mappings().first()

    

@router.post('/',status_code=status.HTTP_200_OK)
def load_in_eshewa(schema:response_model.LoadEshewa,
                   db_eshewa:Session=Depends(db_conn_eshewa.get_db),
                   db_bank:Session=Depends(db_conn_bank.get_db)):
    
    sender_infomation=check_sender_email_status(schema.sender_email,schema.sender_pass)
    if sender_infomation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalied sender credentials")
    
    if sender_infomation["Amount"]<schema.amount:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail="insufficent amount to load")
    
    if check_receive_eshewa_id(schema.receiver_email,db_eshewa) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="no such user in eshewa")
    
    db_bank.execute(text("UPDATE users SET Amount = Amount - :amt WHERE email=:email"),
                    params={"amt":schema.amount,"email":schema.sender_email})
    
    db_eshewa.execute(text("UPDATE user SET amount = amount + :amt WHERE email=:email"),
                         params={"amt":schema.amount,"email":schema.receiver_email})
    

    new_transaction=db_model.Transaction(sender_email=schema.sender_email,
                         receiver_email=schema.receiver_email,
                         amount_transferred=schema.amount,
                         transaction_type="Bank_to_eshewa",
                         transaction_purpose=schema.purpose)
    db_eshewa.add(new_transaction)
    db_eshewa.commit()
    db_bank.commit()
    return {"success":"The money has load sucessfully"}


    



    


