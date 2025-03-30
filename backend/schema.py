from pydantic import BaseModel
from typing import List


class Bill(BaseModel): 
    id = int
    title = str
    bill_type = str
    congress = str
    introduction_date = str
    summary = str

    confidence_score = int
    stage = int
    justification = str
    effect = int
    sectors = str

    class Config:
        orm_mode = True