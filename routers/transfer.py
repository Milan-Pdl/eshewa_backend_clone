
from fastapi import APIRouter,Depends,HTTPException, Query,status
from  sqlalchemy.orm import Session
from sqlalchemy import text
from db_connection import DbConnection
from models import response_model,db_model
from BankGateway.db_conn import DBConnection
from utils.oauth2 import get_user
from servicelogic.service import check_receive_eshewa_id,check_sender_email_status, deduct_from_bank,get_eshewa_user_by_email
from typing import List, Optional

db_conn_bank=DBConnection()
db_conn_eshewa=DbConnection()

router=APIRouter(
    prefix="/loadmoney",
    tags=["bankservices"]
)

@router.post('/',status_code=status.HTTP_200_OK)
def load_bank_to_eshewa(schema:response_model.LoadEshewa,
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
    
    # db_bank.execute(text("UPDATE users SET Amount = Amount - :amt WHERE email=:email"),
    #                 params={"amt":schema.amount,"email":schema.sender_email})

    success = deduct_from_bank(db_bank, schema.sender_email, schema.amount)

    if not success:
        raise HTTPException(status_code=400, detail="Bank deduction failed")
    
    db_eshewa.execute(text("UPDATE user SET amount = amount + :amt WHERE email=:email"),
                         params={"amt":schema.amount,"email":schema.receiver_email})
    
    

    new_transaction=db_model.Transaction(sender_email=schema.sender_email,
                         receiver_email=schema.receiver_email,
                         amount_transferred=schema.amount,
                         transaction_type="Bank_to_eshewa",
                         transaction_purpose=schema.purpose)
    db_eshewa.add(new_transaction)
    db_eshewa.commit()
         
    return {"success":"The money has load sucessfully"}


@router.post('/eshewa', status_code=status.HTTP_200_OK)
def load_money_eshewa_to_eshewa(
    schema: response_model.LoadEshewa,  # sender_email, receiver_email, amount, purpose
    db: Session = Depends(db_conn_eshewa.get_db),
    current_user=Depends(get_user)
):
    print(current_user.email)
    print(type(current_user))
    # Check sender exists
    sender = get_eshewa_user_by_email(schema.sender_email, db)
    if sender is None:
        raise HTTPException(status_code=404, detail="Sender does not exist in eSewa")

    # Check receiver exists
    receiver = get_eshewa_user_by_email(schema.receiver_email, db)
    if receiver is None:
        raise HTTPException(status_code=404, detail="Receiver does not exist in eSewa")

    # 3Check sender has enough balance
    if sender["amount"] < schema.amount:
        raise HTTPException(status_code=406, detail="Insufficient balance in sender wallet")

    # Update balances
    try:
        # Deduct from sender
        db.execute(
            text("UPDATE user SET amount = amount - :amt WHERE email=:email"),
            {"amt": schema.amount, "email": schema.sender_email}
        )

        # Add to receiver
        db.execute(
            text("UPDATE user SET amount = amount + :amt WHERE email=:email"),
            {"amt": schema.amount, "email": schema.receiver_email}
        )

        # Insert transaction record
        transaction = db_model.Transaction(
            sender_email=schema.sender_email,
            receiver_email=schema.receiver_email,
            amount_transferred=schema.amount,
            transaction_type="Eshewa_to_Eshewa",
            transaction_purpose=schema.purpose
        )
        db.add(transaction)

        # Commit all changes
        db.commit()

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Transaction failed: {str(e)}")

    return {
        "success": True,
        "message": f"{schema.amount} has been transferred from {schema.sender_email} to {schema.receiver_email}"
    }

# @router.get("/history",status_code=status.HTTP_202_ACCEPTED,response_model=List[response_model.TransactionResponse])
# def get_user_transaction_history(db:Session=Depends(db_conn_eshewa.get_db),user=Depends(get_user)):
#     user_history=db.execute(text("select * from transactions where sender_email=:sender_email or receiver_email=:receiver_email"),
#                             params={"sender_email":user.email,"receiver_email":user.email}).mappings().all()
    
#     return user_history

@router.get(
    "/history",
    status_code=status.HTTP_200_OK,
    response_model=List[response_model.TransactionResponse]
)
def get_user_transaction_history(
    db: Session = Depends(db_conn_eshewa.get_db),
    user = Depends(get_user),

    #  Filters
    transaction_type: Optional[str] = Query(None),
    min_amount: Optional[float] = Query(None),
    max_amount: Optional[float] = Query(None),

    # Date filters
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),

    #  Pagination
    limit: int = Query(10),
    offset: int = Query(0),

    #  Sorting
    sort_by: str = Query("created_at"),   # column name
    order: str = Query("desc")            # asc / desc
):
    
    base_query = """
    SELECT * FROM transactions
    WHERE (sender_email = :email OR receiver_email = :email)
    """

    params = {"email": user.email}

    # Apply filters
    if transaction_type:
        base_query += " AND transaction_type = :transaction_type"
        params["transaction_type"] = transaction_type

    if min_amount is not None:
        base_query += " AND amount_transferred >= :min_amount"
        params["min_amount"] = min_amount

    if max_amount is not None:
        base_query += " AND amount_transferred <= :max_amount"
        params["max_amount"] = max_amount

    if start_date:
        base_query += " AND created_at >= :start_date"
        params["start_date"] = start_date

    if end_date:
        base_query += " AND created_at <= :end_date"
        params["end_date"] = end_date

    #  Sorting
    if order.lower() not in ["asc", "desc"]:
        order = "desc"

    base_query += f" ORDER BY {sort_by} {order}"

    #  Pagination
    base_query += " LIMIT :limit OFFSET :offset"
    params["limit"] = limit
    params["offset"] = offset

    result = db.execute(text(base_query), params).mappings().all()

    return result