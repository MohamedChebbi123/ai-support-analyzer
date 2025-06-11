from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import upload
from routes.classifieddata import router as classifieddata_router
from connection.database import Base, engine
from routes import fetchclassifieddata

app = FastAPI()
app.add_middleware(
     CORSMiddleware,
    allow_origins=["*"],
     allow_credentials=True,
     allow_methods=["*"],
    allow_headers=["*"],
 )

app.include_router(upload.router)
app.include_router(classifieddata_router)
app.include_router(fetchclassifieddata.router)
Base.metadata.create_all(bind=engine)

