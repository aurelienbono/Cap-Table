from fastapi import FastAPI
from api import token
from database import Base, engine


app = FastAPI(title="Corporate OS - Cap Table API")
Base.metadata.create_all(bind=engine)
app.include_router(token.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Cap Table API"}

 