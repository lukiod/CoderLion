from typing import Dict, Any, List
import asyncio
import time
from app.agents.base import BaseAgent, AgentResult
from app.agents.registry import AgentRegistry

class ReviewOrchestrator:
    def __init__(self):
        self.agent_registry = AgentRegistry()
    
    async def analyze_pull_request(self, pr_data: Dict[str, Any]) -> Dict[str, Any]:
        """Orchestrate analysis of a pull request using all agents"""
        start_time = time.time()
        
        # Extract PR information
        pr_title = pr_data.get('title', '')
        pr_description = pr_data.get('body', '')
        repository = pr_data.get('repository', {}).get('full_name', '')
        
        # Get all file changes
        files = pr_data.get('files', [])
        
        # Run agents in parallel for each file
        all_results = []
        
        for file_data in files:
            file_path = file_data.get('filename', '')
            patch = file_data.get('patch', '')
            
            if not patch:  # Skip files without changes
                continue
            
            # Determine language from file extension
            language = self._detect_language(file_path)
            
            context = {
                'file_path': file_path,
                'language': language,
                'repository': repository,
                'pr_title': pr_title,
                'pr_description': pr_description
            }
            
            # Run all agents in parallel for this file
            file_results = await self._run_agents_for_file(patch, context)
            all_results.extend(file_results)
        
        # Aggregate results
        total_execution_time = int((time.time() - start_time) * 1000)
        
        return {
            'status': 'completed',
            'total_execution_time': total_execution_time,
            'agent_results': all_results,
            'summary': self._generate_summary(all_results),
            'confidence_score': self._calculate_overall_confidence(all_results)
        }
    
    async def _run_agents_for_file(self, code_diff: str, context: Dict[str, Any]) -> List[AgentResult]:
        """Run all agents in parallel for a single file"""
        agents = self.agent_registry.get_all_agents()
        
        # Create tasks for all agents
        tasks = []
        for agent in agents:
            task = asyncio.create_task(agent.analyze(code_diff, context))
            tasks.append(task)
        
        # Wait for all agents to complete
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out exceptions and return valid results
        valid_results = []
        for result in results:
            if isinstance(result, AgentResult):
                valid_results.append(result)
            elif isinstance(result, Exception):
                # Create error result for failed agents
                error_result = AgentResult(
                    agent_name="unknown",
                    status="error",
                    findings=[],
                    confidence_score=0,
                    execution_time=0,
                    error_message=str(result)
                )
                valid_results.append(error_result)
        
        return valid_results
    
    def _detect_language(self, file_path: str) -> str:
        """Detect programming language from file extension"""
        extension_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.jsx': 'javascript',
            '.tsx': 'typescript',
            '.java': 'java',
            '.cpp': 'cpp',
            '.c': 'c',
            '.cs': 'csharp',
            '.go': 'go',
            '.rs': 'rust',
            '.php': 'php',
            '.rb': 'ruby',
            '.swift': 'swift',
            '.kt': 'kotlin',
            '.scala': 'scala',
            '.r': 'r',
            '.m': 'matlab',
            '.sh': 'bash',
            '.sql': 'sql',
            '.html': 'html',
            '.css': 'css',
            '.scss': 'scss',
            '.sass': 'sass',
            '.less': 'less',
            '.xml': 'xml',
            '.json': 'json',
            '.yaml': 'yaml',
            '.yml': 'yaml',
            '.md': 'markdown',
            '.txt': 'text'
        }
        
        # Get file extension
        if '.' in file_path:
            extension = '.' + file_path.split('.')[-1].lower()
            return extension_map.get(extension, 'unknown')
        
        return 'unknown'
    
    def _generate_summary(self, results: List[AgentResult]) -> str:
        """Generate a summary of all agent results"""
        total_findings = sum(len(result.findings) for result in results)
        successful_agents = len([r for r in results if r.status == 'success'])
        warning_agents = len([r for r in results if r.status == 'warning'])
        error_agents = len([r for r in results if r.status == 'error'])
        
        summary = f"Analysis completed with {total_findings} findings across {len(results)} agents. "
        summary += f"Success: {successful_agents}, Warnings: {warning_agents}, Errors: {error_agents}"
        
        return summary
    
    def _calculate_overall_confidence(self, results: List[AgentResult]) -> int:
        """Calculate overall confidence score"""
        if not results:
            return 0
        
        total_confidence = sum(result.confidence_score for result in results)
        return total_confidence // len(results)
