from fastapi import FastAPI


app = FastAPI(title="Corporate OS - Cap Table API")


@app.get("/")
def read_root():
    return {"message": "Welcome to the Cap Table API"}

 