from fastapi import APIRouter, HTTPException, UploadFile, File
import pandas as pd
import io
from sqlalchemy.orm import Session
from connection.database import SessionLocal
from models.data import Data

router = APIRouter()

@router.post("/upload")
async def uploadfile(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Please upload a CSV file.")

    try:
        contents = await file.read()

        df = pd.read_csv(io.StringIO(contents.decode()), delimiter=';')

     
        db = SessionLocal()
        for _, row in df.iterrows():
            try:
                record = Data(
                    name=row["name"],
                    lastname=row["lastname"],
                    country=row["country"],
                    email=row["email"],
                    phone_number=row["phone number"],
                    problem=row["problem"],
                    submission_date=row["submission date"]
                )
                db.add(record)
            except Exception as row_error:
                raise HTTPException(status_code=422, detail=f"Error in row {_}: {str(row_error)}")

        db.commit()
        db.close()

        return {"message": "Data added successfully"}

    except Exception as e:
        raise HTTPException(status_code=422, detail=f"CSV processing error: {str(e)}")
