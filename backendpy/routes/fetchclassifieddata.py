from models.classifieddata import ClassifiedDataByPriority
from connection.database import SessionLocal
from connection.database import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router=APIRouter()

@router.get("/fetchclassifeiddata")
def fetchclassifieddata(db: Session = Depends(get_db)):
    classifeddata=db.query(ClassifiedDataByPriority).all()
    return classifeddata