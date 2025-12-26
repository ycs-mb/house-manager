from crewai import Agent, LLM
from app.core.config import settings
import os

# Define the LLM based on user configuration (Gemini on Vertex AI preferred)
def get_llm():
    if settings.GOOGLE_CLOUD_PROJECT:
        # Use Vertex AI Gemini
        return LLM(
            model=f"vertex_ai/{settings.GEMINI_MODEL}",
            project=settings.GOOGLE_CLOUD_PROJECT,
            location=settings.GOOGLE_CLOUD_REGION
        )
    if settings.OPENAI_API_KEY and settings.OPENAI_API_KEY != "your_openai_key":
        return LLM(model="gpt-4", api_key=settings.OPENAI_API_KEY)
    
    # Fallback for local demo
    return LLM(model="gpt-3.5-turbo", base_url="http://localhost:1234/v1", api_key="dummy")

class FinanceAgent(Agent):
    def __init__(self):
        super().__init__(
            role='Finance Agent',
            goal='Manage and analyze personal finances, budgets, and expenses',
            backstory="""You are a financial expert AI agent. You help users manage 
            their household budget, track expenses, and plan for financial goals.""",
            allow_delegation=True,
            verbose=True,
            llm=get_llm()
        )

class PlannerAgent(Agent):
    def __init__(self):
        super().__init__(
            role='Planner Agent',
            goal='Optimize daily planning and project management',
            backstory="""You are a productivity specialist. You help users organize 
            tasks, manage projects, and optimize their daily schedules using tools 
            like Trello.""",
            allow_delegation=True,
            verbose=True, llm=get_llm()
        )

class CalendarAgent(Agent):
    def __init__(self):
        super().__init__(
            role='Calendar Agent',
            goal='Manage schedules and optimize time management',
            backstory="""You are a calendar management expert. You optimize 
            schedules and manage time-based commitments using Google Calendar.""",
            allow_delegation=True,
            verbose=True, llm=get_llm()
        )

class IdeaAgent(Agent):
    def __init__(self):
        super().__init__(
            role='Idea Agent',
            goal='Capture and develop household and personal ideas',
            backstory="""You are an innovative AI agent specialized in capturing 
            insights and organizing them in Notion.""",
            allow_delegation=True,
            verbose=True, llm=get_llm()
        )

class InventoryAgent(Agent):
    def __init__(self):
        super().__init__(
            role='Inventory Agent',
            goal='Track household inventory and manage shopping lists',
            backstory="""You are a meticulous inventory manager. You track pantry 
            items, monitor expiration dates, and manage shopping lists in Trello.""",
            allow_delegation=True,
            verbose=True, llm=get_llm()
        )

class ChoreCoordinatorAgent(Agent):
    def __init__(self):
        super().__init__(
            role='Chore Coordinator Agent',
            goal='Assign and track household chores fairly',
            backstory="""You are a household operations specialist. You assign 
            chores to family members, track completion in Trello, and manage 
            a rewards system.""",
            allow_delegation=True,
            verbose=True, llm=get_llm()
        )

# Knowledge crew agents
class ReadingAgent(Agent):
    def __init__(self):
        super().__init__(
            role='Reading Agent',
            goal='Optimize reading and learning optimization',
            backstory="""You help users process and retain information from 
            their reading materials effectively.""",
            allow_delegation=True,
            verbose=True, llm=get_llm()
        )

class TechScienceAgent(Agent):
    def __init__(self):
        super().__init__(
            role='Tech Science Agent',
            goal='Track technology and science trends',
            backstory="""You monitor and analyze developments in the tech 
            and science fields.""",
            allow_delegation=True,
            verbose=True, llm=get_llm()
        )

class GeoPoliticsAgent(Agent):
    def __init__(self):
        super().__init__(
            role='Geopolitics Agent',
            goal='Monitor geopolitical developments',
            backstory="""You track and analyze global political and economic 
            trends.""",
            allow_delegation=True,
            verbose=True, llm=get_llm()
        )
