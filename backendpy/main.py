from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import upload

from connection.database import Base, engine
from models.data import Data

app = FastAPI()
app.add_middleware(
     CORSMiddleware,
    allow_origins=["*"],
     allow_credentials=True,
     allow_methods=["*"],
    allow_headers=["*"],
 )

app.include_router(upload.router)
Base.metadata.create_all(bind=engine)

