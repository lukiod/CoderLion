from typing import Dict, Any, List
import time
from app.agents.base import BaseAgent, AgentResult

class SecurityAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="security",
            description="Security vulnerabilities and best practices"
        )
    
    async def analyze(self, code_diff: str, context: Dict[str, Any]) -> AgentResult:
        """Analyze code for security issues"""
        start_time = time.time()
        
        try:
            review_text = await self._generate_review(code_diff, context)
            findings = self._parse_findings(review_text)
            confidence = self._calculate_confidence(findings)
            
            execution_time = int((time.time() - start_time) * 1000)
            
            return AgentResult(
                agent_name=self.name,
                status="success" if not findings else "warning",
                findings=findings,
                confidence_score=confidence,
                execution_time=execution_time
            )
        except Exception as e:
            execution_time = int((time.time() - start_time) * 1000)
            return AgentResult(
                agent_name=self.name,
                status="error",
                findings=[],
                confidence_score=0,
                execution_time=execution_time,
                error_message=str(e)
            )
    
    def get_system_prompt(self) -> str:
        return """You are a security expert code reviewer. Analyze the provided code for security vulnerabilities and issues.

Focus on:
1. SQL injection vulnerabilities
2. Cross-site scripting (XSS) vulnerabilities
3. Authentication and authorization issues
4. Input validation problems
5. Sensitive data exposure
6. Insecure dependencies
7. Cryptographic issues
8. Access control problems
9. Session management issues
10. CSRF vulnerabilities

For each issue found:
- Clearly describe the security risk
- Explain the potential impact
- Provide specific remediation steps
- Rate the severity (critical, high, medium, low)

Be thorough but concise. Prioritize critical and high-severity issues."""
