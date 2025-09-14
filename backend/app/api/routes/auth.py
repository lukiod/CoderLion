from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.services.auth import AuthService
from app.services.github import GitHubService
from pydantic import BaseModel
from typing import Optional

router = APIRouter()
security = HTTPBearer()
auth_service = AuthService()
github_service = GitHubService()

class GitHubCallback(BaseModel):
    code: str
    state: Optional[str] = None

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: dict

@router.post("/github/callback", response_model=TokenResponse)
async def github_callback(callback_data: GitHubCallback, db: Session = Depends(get_db)):
    """Handle GitHub OAuth callback"""
    try:
        # Exchange code for access token
        # This is a simplified implementation - in production, you'd use httpx to make the actual request
        access_token = "github_access_token"  # Replace with actual token exchange
        
        # Get user info from GitHub
        # This is also simplified - you'd use the GitHub API
        github_user = {
            "id": 12345,
            "login": "testuser",
            "email": "test@example.com",
            "avatar_url": "https://avatars.githubusercontent.com/u/12345"
        }
        
        # Check if user exists
        user = db.query(User).filter(User.github_id == github_user["id"]).first()
        
        if not user:
            # Create new user
            user = User(
                github_id=github_user["id"],
                username=github_user["login"],
                email=github_user["email"],
                avatar_url=github_user["avatar_url"],
                access_token=access_token
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        else:
            # Update existing user
            user.access_token = access_token
            db.commit()
        
        # Create JWT token
        jwt_token = auth_service.create_access_token(data={"sub": str(user.id)})
        
        return TokenResponse(
            access_token=jwt_token,
            token_type="bearer",
            user={
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "avatar_url": user.avatar_url
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Authentication failed: {str(e)}"
        )

@router.get("/me")
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get current user information"""
    try:
        user_id = auth_service.get_current_user_id(credentials.credentials)
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "avatar_url": user.avatar_url,
            "created_at": user.created_at
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
