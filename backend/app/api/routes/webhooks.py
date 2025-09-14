from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.repository import Repository
from app.models.review import Review, ReviewComment, ReviewStatus, ReviewType
from app.models.agent import AgentRun
from app.agents.orchestrator import ReviewOrchestrator
from app.services.github import GitHubService
import json
import hmac
import hashlib
from app.core.config import settings

router = APIRouter()
orchestrator = ReviewOrchestrator()
github_service = GitHubService()

def verify_github_signature(payload: bytes, signature: str) -> bool:
    """Verify GitHub webhook signature"""
    if not settings.github_client_secret:
        return True  # Skip verification if no secret is set
    
    expected_signature = hmac.new(
        settings.github_client_secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(f"sha256={expected_signature}", signature)

@router.post("/github")
async def github_webhook(request: Request, db: Session = Depends(get_db)):
    """Handle GitHub webhook events"""
    try:
        # Get the raw body
        body = await request.body()
        
        # Verify signature
        signature = request.headers.get("X-Hub-Signature-256", "")
        if not verify_github_signature(body, signature):
            raise HTTPException(status_code=401, detail="Invalid signature")
        
        # Parse the payload
        payload = json.loads(body)
        event_type = request.headers.get("X-GitHub-Event")
        
        if event_type == "pull_request":
            await handle_pull_request_event(payload, db)
        elif event_type == "pull_request_review":
            await handle_pull_request_review_event(payload, db)
        
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def handle_pull_request_event(payload: dict, db: Session):
    """Handle pull request events"""
    action = payload.get("action")
    pr_data = payload.get("pull_request", {})
    
    if action in ["opened", "synchronize"]:
        # Create or update review
        await create_or_update_review(pr_data, db)
    elif action == "closed":
        # Mark review as completed
        await mark_review_completed(pr_data, db)

async def create_or_update_review(pr_data: dict, db: Session):
    """Create or update a review for a pull request"""
    try:
        # Get repository
        repo_data = pr_data.get("repository", {})
        repo = db.query(Repository).filter(
            Repository.github_id == repo_data.get("id")
        ).first()
        
        if not repo:
            return  # Repository not connected to CodeLion
        
        # Check if review already exists
        review = db.query(Review).filter(
            Review.github_pr_id == pr_data.get("number"),
            Review.repository_id == repo.id
        ).first()
        
        if not review:
            # Create new review
            review = Review(
                github_pr_id=pr_data.get("number"),
                repository_id=repo.id,
                status=ReviewStatus.PENDING
            )
            db.add(review)
            db.commit()
            db.refresh(review)
        
        # Update review status
        review.status = ReviewStatus.IN_PROGRESS
        db.commit()
        
        # Run agent analysis
        await run_agent_analysis(review, pr_data, db)
        
    except Exception as e:
        print(f"Error creating/updating review: {e}")

async def run_agent_analysis(review: Review, pr_data: dict, db: Session):
    """Run agent analysis on the pull request"""
    try:
        # Get the full PR data with files
        repo = review.repository
        owner = repo.full_name.split("/")[0]
        repo_name = repo.full_name.split("/")[1]
        
        full_pr_data = await github_service.get_pull_request(
            owner, repo_name, review.github_pr_id
        )
        
        # Run orchestrator
        analysis_result = await orchestrator.analyze_pull_request(full_pr_data)
        
        # Update review with results
        review.status = ReviewStatus.COMPLETED
        review.summary = analysis_result.get("summary", "")
        review.confidence_score = analysis_result.get("confidence_score", 0)
        db.commit()
        
        # Save agent runs
        for agent_result in analysis_result.get("agent_results", []):
            agent_run = AgentRun(
                review_id=review.id,
                agent_name=agent_result.agent_name,
                status=agent_result.status,
                output_data=agent_result.dict(),
                execution_time=agent_result.execution_time,
                error_message=agent_result.error_message
            )
            db.add(agent_run)
        
        # Save review comments
        for agent_result in analysis_result.get("agent_results", []):
            for finding in agent_result.findings:
                comment = ReviewComment(
                    review_id=review.id,
                    file_path=finding.get("file_path", ""),
                    line_number=finding.get("line_number"),
                    comment_type=ReviewType(agent_result.agent_name),
                    content=finding.get("description", ""),
                    severity=finding.get("severity", "medium")
                )
                db.add(comment)
        
        db.commit()
        
        # Post comments to GitHub
        await post_review_comments(review, db)
        
    except Exception as e:
        print(f"Error running agent analysis: {e}")
        review.status = ReviewStatus.FAILED
        db.commit()

async def post_review_comments(review: Review, db: Session):
    """Post review comments to GitHub"""
    try:
        repo = review.repository
        owner = repo.full_name.split("/")[0]
        repo_name = repo.full_name.split("/")[1]
        
        # Get all comments for this review
        comments = db.query(ReviewComment).filter(
            ReviewComment.review_id == review.id
        ).all()
        
        for comment in comments:
            if comment.line_number and comment.file_path:
                await github_service.post_review_comment(
                    owner, repo_name, review.github_pr_id,
                    comment.file_path, comment.line_number,
                    f"**{comment.comment_type.value.title()} Review**\n\n{comment.content}"
                )
        
    except Exception as e:
        print(f"Error posting review comments: {e}")

async def mark_review_completed(pr_data: dict, db: Session):
    """Mark review as completed when PR is closed"""
    try:
        repo_data = pr_data.get("repository", {})
        repo = db.query(Repository).filter(
            Repository.github_id == repo_data.get("id")
        ).first()
        
        if repo:
            review = db.query(Review).filter(
                Review.github_pr_id == pr_data.get("number"),
                Review.repository_id == repo.id
            ).first()
            
            if review:
                review.status = ReviewStatus.COMPLETED
                db.commit()
    except Exception as e:
        print(f"Error marking review completed: {e}")

async def handle_pull_request_review_event(payload: dict, db: Session):
    """Handle pull request review events"""
    # This could be used to track manual reviews or respond to them
    pass
