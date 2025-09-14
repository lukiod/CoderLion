from github import Github
from typing import Dict, Any, Optional
import httpx
from app.core.config import settings

class GitHubService:
    def __init__(self):
        self.github = Github(settings.github_client_id, settings.github_client_secret)
    
    async def get_pull_request(self, owner: str, repo: str, pr_number: int) -> Dict[str, Any]:
        """Get pull request data from GitHub"""
        try:
            repo_obj = self.github.get_repo(f"{owner}/{repo}")
            pr = repo_obj.get_pull(pr_number)
            
            # Get files changed
            files = []
            for file in pr.get_files():
                files.append({
                    'filename': file.filename,
                    'status': file.status,
                    'additions': file.additions,
                    'deletions': file.deletions,
                    'changes': file.changes,
                    'patch': file.patch
                })
            
            return {
                'id': pr.id,
                'number': pr.number,
                'title': pr.title,
                'body': pr.body or '',
                'state': pr.state,
                'created_at': pr.created_at.isoformat(),
                'updated_at': pr.updated_at.isoformat(),
                'user': {
                    'login': pr.user.login,
                    'id': pr.user.id,
                    'avatar_url': pr.user.avatar_url
                },
                'repository': {
                    'id': repo_obj.id,
                    'name': repo_obj.name,
                    'full_name': repo_obj.full_name,
                    'owner': {
                        'login': repo_obj.owner.login,
                        'id': repo_obj.owner.id
                    }
                },
                'files': files
            }
        except Exception as e:
            raise Exception(f"Error fetching pull request: {str(e)}")
    
    async def create_webhook(self, owner: str, repo: str, webhook_url: str) -> Dict[str, Any]:
        """Create a webhook for the repository"""
        try:
            repo_obj = self.github.get_repo(f"{owner}/{repo}")
            
            webhook = repo_obj.create_hook(
                name="web",
                config={
                    "url": webhook_url,
                    "content_type": "json"
                },
                events=["pull_request", "pull_request_review"],
                active=True
            )
            
            return {
                'id': webhook.id,
                'url': webhook.url,
                'events': webhook.events,
                'active': webhook.active
            }
        except Exception as e:
            raise Exception(f"Error creating webhook: {str(e)}")
    
    async def delete_webhook(self, owner: str, repo: str, webhook_id: int):
        """Delete a webhook"""
        try:
            repo_obj = self.github.get_repo(f"{owner}/{repo}")
            webhook = repo_obj.get_hook(webhook_id)
            webhook.delete()
        except Exception as e:
            raise Exception(f"Error deleting webhook: {str(e)}")
    
    async def post_comment(self, owner: str, repo: str, pr_number: int, comment: str):
        """Post a comment on a pull request"""
        try:
            repo_obj = self.github.get_repo(f"{owner}/{repo}")
            pr = repo_obj.get_pull(pr_number)
            pr.create_issue_comment(comment)
        except Exception as e:
            raise Exception(f"Error posting comment: {str(e)}")
    
    async def post_review_comment(self, owner: str, repo: str, pr_number: int, 
                                 file_path: str, line_number: int, comment: str):
        """Post a review comment on a specific line"""
        try:
            repo_obj = self.github.get_repo(f"{owner}/{repo}")
            pr = repo_obj.get_pull(pr_number)
            
            # Get the commit SHA
            commits = list(pr.get_commits())
            if not commits:
                raise Exception("No commits found in pull request")
            
            commit_sha = commits[-1].sha
            
            pr.create_review_comment(
                body=comment,
                commit=repo_obj.get_commit(commit_sha),
                path=file_path,
                line=line_number
            )
        except Exception as e:
            raise Exception(f"Error posting review comment: {str(e)}")
