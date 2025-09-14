from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base

class ReviewStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class ReviewType(str, enum.Enum):
    SECURITY = "security"
    PERFORMANCE = "performance"
    STYLE = "style"
    BUG = "bug"
    DOCUMENTATION = "documentation"

class Review(Base):
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    github_pr_id = Column(Integer, index=True)
    repository_id = Column(Integer, ForeignKey("repositories.id"))
    status = Column(Enum(ReviewStatus), default=ReviewStatus.PENDING)
    summary = Column(Text)
    confidence_score = Column(Integer)  # 0-100
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    repository = relationship("Repository", back_populates="reviews")
    comments = relationship("ReviewComment", back_populates="review")
    agent_runs = relationship("AgentRun", back_populates="review")

class ReviewComment(Base):
    __tablename__ = "review_comments"
    
    id = Column(Integer, primary_key=True, index=True)
    review_id = Column(Integer, ForeignKey("reviews.id"))
    file_path = Column(String)
    line_number = Column(Integer)
    comment_type = Column(Enum(ReviewType))
    content = Column(Text)
    severity = Column(String)  # low, medium, high, critical
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    review = relationship("Review", back_populates="comments")
