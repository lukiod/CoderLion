from typing import Dict, Any, List
import time
from app.agents.base import BaseAgent, AgentResult

class StyleAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="style",
            description="Code style, formatting, and best practices"
        )
    
    async def analyze(self, code_diff: str, context: Dict[str, Any]) -> AgentResult:
        """Analyze code for style and formatting issues"""
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
        return """You are a code style and best practices expert. Analyze the provided code for style, formatting, and best practice issues.

Focus on:
1. Code formatting and indentation
2. Naming conventions (variables, functions, classes)
3. Code organization and structure
4. Documentation and comments
5. Import organization
6. Function length and complexity
7. Variable declarations and usage
8. Error handling patterns
9. Code duplication
10. Language-specific best practices

For each issue found:
- Explain the style violation
- Suggest improvements
- Provide examples of better code
- Rate the importance (high, medium, low)

Be constructive and focus on maintainability and readability. Consider the programming language and common conventions."""
