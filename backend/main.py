from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
from backend import models
from backend.db import SessionLocal, engine
from sqlalchemy.orm import Session
from httpx import AsyncClient

app = FastAPI()
models.Bill.metadata.create_all(bind = engine)
    
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
    db = SessionLocal()
    try: 
        yield db
    finally: 
        db.close()
db_dependency = Annotated[Session, Depends(get_db)]

async def upload_bills(data: Bill):
    async with AsyncClient() as client:
           try:
            res = await client.post('http://localhost:5432/create_bill', data = data)
            return res
           except ValueError as e:
                print(e)
                raise HTTPException(status_code=401, detail="error")
               
               
     


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
    except ValueError as e:
        print(e)
        raise HTTPException(status_code=404, detail="Failed to create bill")
    
    

@app.get('/all_bills')
async def get_bills(bills: Bill, db: db_dependency):
    res = db.query(models.Bill).all()
    if not res:
        raise HTTPException(status=404, detail = 'Error lmao')
    return res

@app.get('/bill/{bill_id}')
async def get_bill(bill_id: int, db: db_dependency):
    res = db.query(models.Bill).filter(models.Bill.id == bill_id).first()
    if not res:
        raise HTTPException(status=404, detail = 'Error lmao')
    return res

app.delete('/delete_bill')
async def delete_bill(bill_id: int, db: db_dependency):
    res = db.query(models.Bill).filter(models.Bill.id == bill_id).delete()
    if not res:
        raise HTTPException(status=404, detail='Error lmao')
    return res