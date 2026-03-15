from fastapi import FastAPI,Depends,status,HTTPException,APIRouter
from sqlalchemy.orm import Session
from BankGateway.db_conn import DBConnection
from sqlalchemy import text
db_con=DBConnection()

router=APIRouter(
    prefix='/bank',
    tags=['Bankgateway']
)

@router.get('/users')
async def get_users(db:Session=Depends(db_con.get_db)):
    try:
        result=db.execute(text("select * from users")).mappings().all()
        return result
    except Exception as e:
        print(e)

