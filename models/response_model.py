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
    
# class Register:


