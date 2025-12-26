from crewai import Crew
from typing import List
from pick_e.agents.specialized_agents import (
    FinanceAgent, PlannerAgent, CalendarAgent,
    IdeaAgent, ReadingAgent, TechScienceAgent, GeoPoliticsAgent
)

class PersonalManagementCrew(Crew):
    def __init__(self):
        self.finance_agent = FinanceAgent()
        self.planner_agent = PlannerAgent()
        self.calendar_agent = CalendarAgent()
        
        super().__init__(
            agents=[self.finance_agent, self.planner_agent, self.calendar_agent],
            tasks=[],  # Tasks will be assigned dynamically by ManagerAgent
            verbose=True
        )

class KnowledgeCrew(Crew):
    def __init__(self):
        self.idea_agent = IdeaAgent()
        self.reading_agent = ReadingAgent()
        self.tech_science_agent = TechScienceAgent()
        self.geopolitics_agent = GeoPoliticsAgent()
        
        super().__init__(
            agents=[
                self.idea_agent, self.reading_agent,
                self.tech_science_agent, self.geopolitics_agent
            ],
            tasks=[],  # Tasks will be assigned dynamically by ManagerAgent
            verbose=True
        )
