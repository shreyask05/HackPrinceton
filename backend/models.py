from typing import Annotated, List
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY

from . import db

class Bill(db.Base):

    __tablename__ = 'Bills'
    id = Column(Integer,primary_key=True,nullable=False)
    title = Column(String, index = True)
    bill_type = Column(String, index = True)
    congress = Column(String, index = True)
    introduction_date = Column(String, index = True)
    summary = Column(String, index = True)
    confidence_score = Column(Integer, index = True)
    stage = Column(String, index = True)
    justification = Column(String, index = True)
    effect= Column(String, index = True)
    sectors =Column(ARRAY(String), index = True)

