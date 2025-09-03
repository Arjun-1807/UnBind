from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from .analysis import AnalysisResponse

class DocumentBase(BaseModel):
    filename: str

class DocumentCreate(DocumentBase):
    pass

class DocumentUpdate(BaseModel):
    filename: Optional[str] = None

class DocumentResponse(DocumentBase):
    id: int
    user_id: int
    original_filename: str
    file_path: str
    file_size: int
    mime_type: str
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    analyses: List[AnalysisResponse] = []

    class Config:
        from_attributes = True
