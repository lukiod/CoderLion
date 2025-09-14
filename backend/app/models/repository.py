from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Repository(Base):
    __tablename__ = "repositories"
    
    id = Column(Integer, primary_key=True, index=True)
    github_id = Column(Integer, unique=True, index=True)
    name = Column(String, index=True)
    full_name = Column(String, unique=True, index=True)
    description = Column(String)
    private = Column(Boolean, default=False)
    html_url = Column(String)
    clone_url = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    is_active = Column(Boolean, default=True)
    webhook_id = Column(Integer)  # GitHub webhook ID
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    owner = relationship("User", back_populates="repositories")
    reviews = relationship("Review", back_populates="repository")
