from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class AnalysisBase(BaseModel):
    analysis_type: str
    simplified_text: str

class AnalysisCreate(AnalysisBase):
    document_id: int
    original_text: Optional[str] = None
    analysis_data: Optional[Dict[str, Any]] = None
    confidence_score: Optional[int] = None

class AnalysisResponse(AnalysisBase):
    id: int
    document_id: int
    original_text: Optional[str] = None
    analysis_data: Optional[Dict[str, Any]] = None
    confidence_score: Optional[int] = None
    processing_time: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True
