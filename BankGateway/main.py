from fastapi import FastAPI
from BankGateway.routers import user_info 

app=FastAPI()
app.include_router(user_info.router)