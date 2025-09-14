from typing import Dict, List, Type
from app.agents.base import BaseAgent
from app.agents.security import SecurityAgent
from app.agents.performance import PerformanceAgent
from app.agents.style import StyleAgent

class AgentRegistry:
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self._register_default_agents()
    
    def _register_default_agents(self):
        """Register default agents"""
        self.register_agent(SecurityAgent())
        self.register_agent(PerformanceAgent())
        self.register_agent(StyleAgent())
    
    def register_agent(self, agent: BaseAgent):
        """Register a new agent"""
        self.agents[agent.name] = agent
    
    def get_agent(self, name: str) -> BaseAgent:
        """Get agent by name"""
        return self.agents.get(name)
    
    def get_all_agents(self) -> List[BaseAgent]:
        """Get all registered agents"""
        return list(self.agents.values())
    
    def get_agent_names(self) -> List[str]:
        """Get all agent names"""
        return list(self.agents.keys())
    
    def unregister_agent(self, name: str):
        """Unregister an agent"""
        if name in self.agents:
            del self.agents[name]
