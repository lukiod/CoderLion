from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
import time
import asyncio
from app.services.gemini import GeminiService

class AgentResult(BaseModel):
    agent_name: str
    status: str  # success, warning, error
    findings: List[Dict[str, Any]]
    confidence_score: int  # 0-100
    execution_time: int  # milliseconds
    error_message: Optional[str] = None

class BaseAgent(ABC):
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.gemini_service = GeminiService()
    
    @abstractmethod
    async def analyze(self, code_diff: str, context: Dict[str, Any]) -> AgentResult:
        """Analyze code and return findings"""
        pass
    
    @abstractmethod
    def get_system_prompt(self) -> str:
        """Get the system prompt for this agent"""
        pass
    
    async def _generate_review(self, code_diff: str, context: Dict[str, Any]) -> str:
        """Generate review using Gemini"""
        system_prompt = self.get_system_prompt()
        
        user_prompt = f"""
        Analyze the following code changes:
        
        File: {context.get('file_path', 'Unknown')}
        Language: {context.get('language', 'Unknown')}
        
        Code Diff:
        {code_diff}
        
        Context:
        - Repository: {context.get('repository', 'Unknown')}
        - PR Title: {context.get('pr_title', 'Unknown')}
        - PR Description: {context.get('pr_description', 'None')}
        
        Please provide a detailed analysis focusing on {self.description.lower()}.
        """
        
        return await self.gemini_service.generate_review(system_prompt, user_prompt)
    
    def _parse_findings(self, review_text: str) -> List[Dict[str, Any]]:
        """Parse the review text into structured findings"""
        # This is a simplified parser - in production, you'd want more sophisticated parsing
        findings = []
        
        # Split by lines and look for issues
        lines = review_text.split('\n')
        current_finding = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Look for severity indicators
            if any(keyword in line.lower() for keyword in ['critical', 'high', 'medium', 'low']):
                if current_finding:
                    findings.append(current_finding)
                
                severity = 'medium'
                if 'critical' in line.lower():
                    severity = 'critical'
                elif 'high' in line.lower():
                    severity = 'high'
                elif 'low' in line.lower():
                    severity = 'low'
                
                current_finding = {
                    'severity': severity,
                    'description': line,
                    'suggestion': '',
                    'line_number': None
                }
            elif current_finding and line.startswith('-'):
                current_finding['suggestion'] = line[1:].strip()
            elif current_finding:
                current_finding['description'] += ' ' + line
        
        if current_finding:
            findings.append(current_finding)
        
        return findings
    
    def _calculate_confidence(self, findings: List[Dict[str, Any]]) -> int:
        """Calculate confidence score based on findings"""
        if not findings:
            return 100  # No issues found
        
        # Simple confidence calculation based on severity
        total_score = 0
        for finding in findings:
            severity_scores = {'critical': 20, 'high': 40, 'medium': 60, 'low': 80}
            total_score += severity_scores.get(finding.get('severity', 'medium'), 60)
        
        return min(100, total_score // len(findings))
