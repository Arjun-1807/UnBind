from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Analysis(Base):
    __tablename__ = "analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    analysis_type = Column(String, nullable=False)  # summary, risk_assessment, compliance_check
    original_text = Column(Text, nullable=True)
    simplified_text = Column(Text, nullable=False)
    analysis_data = Column(JSON, nullable=True)  # Additional structured data
    confidence_score = Column(Integer, nullable=True)  # 0-100
    processing_time = Column(Integer, nullable=True)  # in seconds
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    document = relationship("Document", back_populates="analyses")
    
    def __repr__(self):
        return f"<Analysis(id={self.id}, document_id={self.document_id}, type='{self.analysis_type}')>"
