from typing import Dict, Any, List
import time
from app.agents.base import BaseAgent, AgentResult

class PerformanceAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="performance",
            description="Performance optimization and efficiency"
        )
    
    async def analyze(self, code_diff: str, context: Dict[str, Any]) -> AgentResult:
        """Analyze code for performance issues"""
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
        return """You are a performance optimization expert. Analyze the provided code for performance issues and optimization opportunities.

Focus on:
1. Algorithm complexity (Big O notation)
2. Database query optimization
3. Memory usage and leaks
4. Caching opportunities
5. Async/await usage
6. Loop optimization
7. String concatenation efficiency
8. File I/O operations
9. Network request optimization
10. Resource cleanup

For each issue found:
- Explain the performance impact
- Suggest specific optimizations
- Provide code examples when helpful
- Rate the impact (high, medium, low)

Consider the context of the application and provide practical, actionable recommendations."""
