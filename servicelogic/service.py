
import requests
from  sqlalchemy.orm import Session
from sqlalchemy import text


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

    
def get_eshewa_user_by_email(email: str, db: Session):
    return db.execute(
        text("SELECT * FROM user WHERE email=:email"),
        {"email": email}
    ).mappings().first()

