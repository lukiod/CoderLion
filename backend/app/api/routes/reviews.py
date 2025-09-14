from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.review import Review, ReviewComment
from app.models.repository import Repository
from app.models.user import User
from app.services.auth import AuthService
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter()
security = HTTPBearer()
auth_service = AuthService()

class ReviewResponse(BaseModel):
    id: int
    github_pr_id: int
    repository_name: str
    status: str
    summary: Optional[str]
    confidence_score: Optional[int]
    created_at: str
    updated_at: str

class ReviewCommentResponse(BaseModel):
    id: int
    file_path: str
    line_number: Optional[int]
    comment_type: str
    content: str
    severity: str
    created_at: str

class ReviewDetailResponse(ReviewResponse):
    comments: List[ReviewCommentResponse]
    agent_runs: List[dict]

@router.get("/", response_model=List[ReviewResponse])
async def get_reviews(
    repository_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    limit: int = Query(20, le=100),
    offset: int = Query(0, ge=0),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get reviews with optional filtering"""
    try:
        user_id = auth_service.get_current_user_id(credentials.credentials)
        
        # Build query
        query = db.query(Review).join(Repository).filter(
            Repository.owner_id == user_id
        )
        
        if repository_id:
            query = query.filter(Review.repository_id == repository_id)
        
        if status:
            query = query.filter(Review.status == status)
        
        # Apply pagination
        reviews = query.order_by(Review.created_at.desc()).offset(offset).limit(limit).all()
        
        return [
            ReviewResponse(
                id=review.id,
                github_pr_id=review.github_pr_id,
                repository_name=review.repository.full_name,
                status=review.status.value,
                summary=review.summary,
                confidence_score=review.confidence_score,
                created_at=review.created_at.isoformat(),
                updated_at=review.updated_at.isoformat() if review.updated_at else review.created_at.isoformat()
            )
            for review in reviews
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/{review_id}", response_model=ReviewDetailResponse)
async def get_review_detail(
    review_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get detailed review information"""
    try:
        user_id = auth_service.get_current_user_id(credentials.credentials)
        
        review = db.query(Review).join(Repository).filter(
            Review.id == review_id,
            Repository.owner_id == user_id
        ).first()
        
        if not review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Review not found"
            )
        
        # Get comments
        comments = db.query(ReviewComment).filter(
            ReviewComment.review_id == review_id
        ).all()
        
        # Get agent runs
        agent_runs = [
            {
                "id": run.id,
                "agent_name": run.agent_name,
                "status": run.status,
                "execution_time": run.execution_time,
                "error_message": run.error_message,
                "created_at": run.created_at.isoformat(),
                "completed_at": run.completed_at.isoformat() if run.completed_at else None
            }
            for run in review.agent_runs
        ]
        
        return ReviewDetailResponse(
            id=review.id,
            github_pr_id=review.github_pr_id,
            repository_name=review.repository.full_name,
            status=review.status.value,
            summary=review.summary,
            confidence_score=review.confidence_score,
            created_at=review.created_at.isoformat(),
            updated_at=review.updated_at.isoformat() if review.updated_at else review.created_at.isoformat(),
            comments=[
                ReviewCommentResponse(
                    id=comment.id,
                    file_path=comment.file_path,
                    line_number=comment.line_number,
                    comment_type=comment.comment_type.value,
                    content=comment.content,
                    severity=comment.severity,
                    created_at=comment.created_at.isoformat()
                )
                for comment in comments
            ],
            agent_runs=agent_runs
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/stats/summary")
async def get_review_stats(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get review statistics for the user"""
    try:
        user_id = auth_service.get_current_user_id(credentials.credentials)
        
        # Get total reviews
        total_reviews = db.query(Review).join(Repository).filter(
            Repository.owner_id == user_id
        ).count()
        
        # Get reviews by status
        status_counts = {}
        for status in ["pending", "in_progress", "completed", "failed"]:
            count = db.query(Review).join(Repository).filter(
                Repository.owner_id == user_id,
                Review.status == status
            ).count()
            status_counts[status] = count
        
        # Get average confidence score
        avg_confidence = db.query(Review).join(Repository).filter(
            Repository.owner_id == user_id,
            Review.confidence_score.isnot(None)
        ).with_entities(Review.confidence_score).all()
        
        avg_confidence_score = 0
        if avg_confidence:
            avg_confidence_score = sum(score[0] for score in avg_confidence) / len(avg_confidence)
        
        # Get total comments
        total_comments = db.query(ReviewComment).join(Review).join(Repository).filter(
            Repository.owner_id == user_id
        ).count()
        
        return {
            "total_reviews": total_reviews,
            "status_counts": status_counts,
            "average_confidence_score": round(avg_confidence_score, 2),
            "total_comments": total_comments
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
