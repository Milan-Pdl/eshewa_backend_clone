from pydantic import BaseModel,EmailStr
from datetime import datetime
 
#userresponse model 
class user(BaseModel):
    email:EmailStr
    password:str

class UserResponse(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime

class LoadEshewa(BaseModel):
    sender_email:EmailStr
    sender_pass:str
    receiver_email:EmailStr
    amount:int
    purpose:str



# class Transactions:
#     # this class is for respone model in loading money

# # class Register:


