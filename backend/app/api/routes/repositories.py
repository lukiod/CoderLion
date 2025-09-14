from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.repository import Repository
from app.models.user import User
from app.services.auth import AuthService
from app.services.github import GitHubService
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()
security = HTTPBearer()
auth_service = AuthService()
github_service = GitHubService()

class RepositoryResponse(BaseModel):
    id: int
    name: str
    full_name: str
    description: Optional[str]
    private: bool
    html_url: str
    is_active: bool
    created_at: str

class ConnectRepositoryRequest(BaseModel):
    owner: str
    repo: str

@router.get("/", response_model=List[RepositoryResponse])
async def get_repositories(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get all repositories for the current user"""
    try:
        user_id = auth_service.get_current_user_id(credentials.credentials)
        
        repositories = db.query(Repository).filter(
            Repository.owner_id == user_id,
            Repository.is_active == True
        ).all()
        
        return [
            RepositoryResponse(
                id=repo.id,
                name=repo.name,
                full_name=repo.full_name,
                description=repo.description,
                private=repo.private,
                html_url=repo.html_url,
                is_active=repo.is_active,
                created_at=repo.created_at.isoformat()
            )
            for repo in repositories
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/connect")
async def connect_repository(
    request: ConnectRepositoryRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Connect a GitHub repository to CodeLion"""
    try:
        user_id = auth_service.get_current_user_id(credentials.credentials)
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Check if repository is already connected
        existing_repo = db.query(Repository).filter(
            Repository.full_name == f"{request.owner}/{request.repo}"
        ).first()
        
        if existing_repo:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Repository already connected"
            )
        
        # Get repository info from GitHub
        # This is simplified - in production, you'd use the actual GitHub API
        repo_data = {
            "id": 12345,  # Replace with actual repo ID
            "name": request.repo,
            "full_name": f"{request.owner}/{request.repo}",
            "description": "Sample repository",
            "private": False,
            "html_url": f"https://github.com/{request.owner}/{request.repo}",
            "clone_url": f"https://github.com/{request.owner}/{request.repo}.git"
        }
        
        # Create repository record
        repository = Repository(
            github_id=repo_data["id"],
            name=repo_data["name"],
            full_name=repo_data["full_name"],
            description=repo_data["description"],
            private=repo_data["private"],
            html_url=repo_data["html_url"],
            clone_url=repo_data["clone_url"],
            owner_id=user_id
        )
        
        db.add(repository)
        db.commit()
        db.refresh(repository)
        
        # Create webhook
        webhook_url = f"https://your-domain.com/api/webhooks/github"
        webhook = await github_service.create_webhook(
            request.owner, request.repo, webhook_url
        )
        
        repository.webhook_id = webhook["id"]
        db.commit()
        
        return {
            "message": "Repository connected successfully",
            "repository": RepositoryResponse(
                id=repository.id,
                name=repository.name,
                full_name=repository.full_name,
                description=repository.description,
                private=repository.private,
                html_url=repository.html_url,
                is_active=repository.is_active,
                created_at=repository.created_at.isoformat()
            )
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.delete("/{repository_id}")
async def disconnect_repository(
    repository_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Disconnect a repository from CodeLion"""
    try:
        user_id = auth_service.get_current_user_id(credentials.credentials)
        
        repository = db.query(Repository).filter(
            Repository.id == repository_id,
            Repository.owner_id == user_id
        ).first()
        
        if not repository:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Repository not found"
            )
        
        # Delete webhook if it exists
        if repository.webhook_id:
            owner = repository.full_name.split("/")[0]
            repo_name = repository.full_name.split("/")[1]
            await github_service.delete_webhook(owner, repo_name, repository.webhook_id)
        
        # Mark repository as inactive
        repository.is_active = False
        db.commit()
        
        return {"message": "Repository disconnected successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
