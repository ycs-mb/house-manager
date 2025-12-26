from crewai import Agent

class FinanceAgent(Agent):
    def __init__(self):
        super().__init__(
            role='Finance Agent',
            goal='Manage and analyze personal finances, investments, and financial planning',
            backstory="""You are a financial expert AI agent specializing in personal 
            finance management, investment analysis, and financial planning. You help users 
            make informed financial decisions and maintain their financial health.""",
            allow_delegation=True,
            verbose=True
        )

class PlannerAgent(Agent):
    def __init__(self):
        super().__init__(
            role='Planner Agent',
            goal='Optimize daily planning and task management',
            backstory="""You are a planning specialist AI agent focused on helping users 
            organize their time, manage tasks, and achieve their goals effectively.""",
            allow_delegation=True,
            verbose=True
        )

class IdeaAgent(Agent):
    def __init__(self):
        super().__init__(
            role='Idea Agent',
            goal='Capture and develop ideas and insights',
            backstory="""You are an innovative AI agent specialized in capturing, 
            organizing, and developing ideas. You help users maintain and expand their 
            knowledge base.""",
            allow_delegation=True,
            verbose=True
        )

class ReadingAgent(Agent):
    def __init__(self):
        super().__init__(
            role='Reading Agent',
            goal='Optimize reading and learning experiences',
            backstory="""You are a reading optimization AI agent that helps users 
            process and retain information from their reading materials more effectively.""",
            allow_delegation=True,
            verbose=True
        )

class TechScienceAgent(Agent):
    def __init__(self):
        super().__init__(
            role='Tech Science Agent',
            goal='Track and analyze technology and science developments',
            backstory="""You are a technology and science specialist AI agent that 
            monitors and analyzes developments in the tech and science fields.""",
            allow_delegation=True,
            verbose=True
        )

class GeoPoliticsAgent(Agent):
    def __init__(self):
        super().__init__(
            role='Geopolitics Agent',
            goal='Monitor and analyze geopolitical developments',
            backstory="""You are a geopolitical analyst AI agent that tracks and 
            analyzes global political and economic developments.""",
            allow_delegation=True,
            verbose=True
        )

class CalendarAgent(Agent):
    def __init__(self):
        super().__init__(
            role='Calendar Agent',
            goal='Manage calendar and scheduling optimization',
            backstory="""You are a calendar management AI agent specialized in 
            optimizing schedules and managing time-based commitments.""",
            allow_delegation=True,
            verbose=True
        )
