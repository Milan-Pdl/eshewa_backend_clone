from pydantic import BaseModel,EmailStr,Field
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

class TransactionResponse(BaseModel):
    transaction_id: int = Field(..., description="Unique identifier for the transaction")
    sender_email: EmailStr = Field(..., description="Email address of the sender")
    receiver_email: EmailStr = Field(..., description="Email address of the receiver")
    amount_transferred: int = Field(..., gt=0, description="The monetary value sent")
    transaction_type: str = Field(..., description="e.g., Transfer, Payment, Refund")
    transaction_purpose: str = Field(..., description="The reason for the transaction")
    transaction_timestamp: datetime = Field(..., description="ISO 8601 formatted date and time")

    class Config:
        # This allows the model to work with database objects (ORMs) easily
        from_attributes = True


# class Transactions:
#     # this class is for respone model in loading money

# # class Register:


