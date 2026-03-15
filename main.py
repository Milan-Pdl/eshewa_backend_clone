from fastapi import FastAPI
from models import db_model,response_model
from routers import user,authentication,service
from db_connection import DbConnection
db_con=DbConnection()
db_model.Base.metadata.create_all(db_con.engine)

# Insert a user
# with next(db_con.get_db()) as db:
#     new_user = db_model.User(email="milan@example.com", password="secret")
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     print(new_user)

app=FastAPI()
app.include_router(user.router)
app.include_router(authentication.router)
app.include_router(service.router)
