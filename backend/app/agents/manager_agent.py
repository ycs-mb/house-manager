from typing import List, Dict, Any, Optional
from crewai import Task
from .specialized_crews import PersonalManagementCrew, KnowledgeCrew, HouseManagementCrew
from app.core.config import settings

class ManagerAgent:
    def __init__(self):
        print("ManagerAgent initialized with CrewAI support")
        self.personal_crew = PersonalManagementCrew()
        self.knowledge_crew = KnowledgeCrew()
        self.house_crew = HouseManagementCrew()

    def _interpret_request(self, request: str) -> str:
        """
        Simple keyword-based routing for local run. 
        In production, this would be an LLM-based classifier.
        """
        request_lc = request.lower()
        
        knowledge_keywords = ['learn', 'what is', 'how does', 'explain', 'geopolitics', 'tech', 'science', 'idea', 'research']
        house_keywords = ['chore', 'clean', 'inventory', 'milk', 'eggs', 'pantry', 'stock', 'shopping']
        personal_keywords = ['finance', 'budget', 'plan', 'calendar', 'schedule', 'meeting', 'task', 'todo']
        
        if any(k in request_lc for k in knowledge_keywords):
            return "knowledge"
        if any(k in request_lc for k in house_keywords):
            return "house"
        if any(k in request_lc for k in personal_keywords):
            return "personal"
            
        return "knowledge" # Default to knowledge

    async def process_request(self, request: str):
        print(f"Processing request: {request}")
        
        # 1. Interpret which crew should handle this
        crew_type = self._interpret_request(request)
        
        # 2. Select the crew
        if crew_type == "house":
            crew = self.house_crew
            agent_name = "ChoreCoordinatorAgent"
        elif crew_type == "personal":
            crew = self.personal_crew
            agent_name = "PlannerAgent"
        else:
            crew = self.knowledge_crew
            agent_name = "ReadingAgent"

        # 3. Create a dynamic task for the preferred agent in that crew
        # Note: CrewAI agents are already defined in specialized_agents
        task = Task(
            description=f"Process the user request: {request}. Provide a helpful, detailed response.",
            expected_output="A helpful and informative response to the user's request.",
            agent=crew.agents[0] # Simplification for now: assign to the first agent in crew
        )
        
        # Add task to crew
        crew.tasks = [task]

        try:
            # 4. Kick off the crew
            # results = crew.kickoff() # CrewAI's kickoff is often blocking, but let's assume it works here
            # In a real async environment, you'd run this in a threadpool
            import asyncio
            from concurrent.futures import ThreadPoolExecutor
            
            loop = asyncio.get_event_loop()
            with ThreadPoolExecutor() as pool:
                result = await loop.run_in_executor(pool, crew.kickoff)
                
            return {
                "status": "success",
                "messages": [{"role": "assistant", "content": str(result)}],
                "results": [{"agent": crew_type, "output": str(result)}]
            }
        except Exception as e:
            print(f"Error in ManagerAgent: {e}")
            # Fallback if OpenAI key is missing or other issue
            return {
                "status": "partial_success",
                "messages": [{"role": "assistant", "content": f"I understood you want to {request}. However, I encountered an issue accessing my full processing capabilities. Here is a basic response: Getting started with something new is always exciting! I recommend breaking it down into small steps."}],
                "results": [{"agent": "ManagerAgent", "output": f"Error: {str(e)}"}]
            }
