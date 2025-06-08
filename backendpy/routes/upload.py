from fastapi import APIRouter, UploadFile, File
import pandas as pd
import io

router=APIRouter()

@router.post("/upload")
async def uploadfile(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        return {"message":"Literally told u to upload csv file"}
    try:
        contents=await file.read()
        
        df=pd.read_csv(io.StringIO(contents.decode()))
        data=df.to_string()
        print(data)
    except Exception as e:
        return {"message":f"errr in csv file : {str(e)}"}