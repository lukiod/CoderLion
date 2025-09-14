from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
import uvicorn

from app.core.config import settings
from app.core.database import engine, Base
from app.api.routes import auth, repositories, reviews, webhooks
from app.agents.registry import AgentRegistry

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="CodeLion API",
    description="AI-powered code review tool with multi-agent architecture",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://frontend:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Initialize agent registry
agent_registry = AgentRegistry()

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(repositories.router, prefix="/api/repositories", tags=["repositories"])
app.include_router(reviews.router, prefix="/api/reviews", tags=["reviews"])
app.include_router(webhooks.router, prefix="/api/webhooks", tags=["webhooks"])

@app.get("/")
async def root():
    return {"message": "CodeLion API is running! 🦁"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "agents": len(agent_registry.agents)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
