from crewai import Crew
from .specialized_agents import (
    FinanceAgent, PlannerAgent, CalendarAgent,
    IdeaAgent, ReadingAgent, TechScienceAgent, GeoPoliticsAgent,
    InventoryAgent, ChoreCoordinatorAgent
)

class PersonalManagementCrew(Crew):
    def __init__(self):
        super().__init__(
            agents=[FinanceAgent(), PlannerAgent(), CalendarAgent()],
            tasks=[],  # Assigned dynamically
            verbose=True
        )

class KnowledgeCrew(Crew):
    def __init__(self):
        super().__init__(
            agents=[IdeaAgent(), ReadingAgent(), TechScienceAgent(), GeoPoliticsAgent()],
            tasks=[],  # Assigned dynamically
            verbose=True
        )

class HouseManagementCrew(Crew):
    def __init__(self):
        super().__init__(
            agents=[InventoryAgent(), ChoreCoordinatorAgent()],
            tasks=[],  # Assigned dynamically
            verbose=True
        )
