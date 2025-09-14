from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class AgentRun(Base):
    __tablename__ = "agent_runs"
    
    id = Column(Integer, primary_key=True, index=True)
    review_id = Column(Integer, ForeignKey("reviews.id"))
    agent_name = Column(String, index=True)
    status = Column(String)  # pending, running, completed, failed
    input_data = Column(JSON)
    output_data = Column(JSON)
    execution_time = Column(Integer)  # milliseconds
    error_message = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))
    
    # Relationships
    review = relationship("Review", back_populates="agent_runs")
