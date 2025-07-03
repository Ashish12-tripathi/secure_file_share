from fastapi import FastAPI
from .database import Base, engine
from .routes import ops, client
import os

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(ops.router)
app.include_router(client.router)

if not os.path.exists("files"):
    os.makedirs("files")

@app.get("/")
def read_root():
    return {"message": "Secure File Sharing API is running"}
