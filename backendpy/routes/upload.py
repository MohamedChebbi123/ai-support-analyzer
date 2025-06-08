from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
import pandas as pd
import io
from sqlalchemy.orm import Session
from connection.database import SessionLocal, get_db
from models.data import Data

router=APIRouter()

@router.post("/upload")
async def uploadfile(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        return {"message":"Literally told u to upload csv file"}
    try:
        contents=await file.read()
        
        df=pd.read_csv(io.StringIO(contents.decode()))
    
        required_columns={"Name","Age","City"}
        if not required_columns.issubset(df.columns):
            raise HTTPException(status_code=400, detail="CSV must have Name, Age, and City columns.")
        db=SessionLocal()
        for _, row in df.iterrows():
            record = Data(name=row["Name"], age=int(row["Age"]), city=row["City"])
            db.add(record)
        db.commit()
        db.close()  
        return{"message":"data added succesfully"} 
    except Exception as e:
        return {"message":f"errr in csv file : {str(e)}"}