from sqlalchemy import Column, Integer, String, DateTime,BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(20), unique=True, nullable=False)
    password = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    amount = Column(BigInteger, default=0)
    account_number = Column(BigInteger, unique=True, nullable=False)
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}')>"

class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(BigInteger, primary_key=True, autoincrement=True)
    sender_email = Column(String(55))
    receiver_email = Column(String(55))
    amount_transferred = Column(BigInteger)
    transaction_type = Column(String(50))
    transaction_purpose = Column(String(255))
    transaction_timestamp = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"<Transaction(id={self.transaction_id}, type='{self.transaction_type}', status='{self.transaction_status}')>"