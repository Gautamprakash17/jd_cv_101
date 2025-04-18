from pydantic import BaseModel
from typing import List
from fastapi import UploadFile

class CVProcessingResult(BaseModel):
    processed: int
    skipped: int
    message: str

class CandidateInfo(BaseModel):
    name: str
    phone: str
    email: str
    score: float
