from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
from backend import models, db
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import ARRAY

app = FastAPI()

models.Bill.metadata.create_all(bind = db.engine)
    

class Bill(BaseModel): 
    id: int
    title: str
    bill_type: str
    congress: str
    introduction_date: str
    summary: str

    confidence_score: int
    stage: int
    justification: str
    effect: int
    sectors: List[str]


def get_db():
    db = db.SessionLocal()
    try: 
        yield db
    finally: 
        db.close()
db_dependency = Annotated[Session, Depends(get_db)]

@app.post("/create_bill")
async def create_bill(bill: Bill, db: db_dependency):
    db_bill = models.Bill(
        id=bill.id,
        title=bill.title,
        bill_type=bill.bill_type,
        congress=bill.congress,
        introduction_date=bill.introduction_date,
        summary=bill.summary,
        confidence_score=bill.confidence_score,
        stage=bill.stage,
        justification=bill.justification,
        effect=bill.effect,
        sectors=bill.sectors
    )
    try:
        db.add(db_bill)
        db.commit()
        db.refresh(db_bill)
        return db_bill
    except:
        raise HTTPException(status_code=400, detail=f"Failed to create bill")

# get all bills
# get certain bill
# upload bill
# delete bill
# 
@app.get('/all_bills')
async def get_bills(bills: Bill, db: db_dependency):
    res = db.query(models.Bill).all()
    if not res:
        raise HTTPException(status)