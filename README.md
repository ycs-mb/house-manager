# Personal Intelligent Companion & Knowledge Ecosystem (PICK-E)

PICK-E is a fully autonomous digital ecosystem for personal productivity, financial management, knowledge capture, reading and learning optimization, daily planning, calendar integration, and insights gathering, orchestrated by a centralized ManagerAgent.

## Features

- **ManagerAgent**: Central orchestrator that dynamically assigns requests to appropriate agents/crews
- **Specialized Agents**:
  - FinanceAgent: Personal finance management and investment analysis
  - PlannerAgent: Daily planning and task management
  - IdeaAgent: Knowledge capture and idea development
  - ReadingAgent: Reading and learning optimization
  - TechScienceAgent: Technology and science tracking
  - GeoPoliticsAgent: Geopolitical analysis
  - CalendarAgent: Calendar management

- **Specialized Crews**:
  - PersonalManagementCrew: Combines FinanceAgent, PlannerAgent, and CalendarAgent
  - KnowledgeCrew: Combines IdeaAgent, ReadingAgent, TechScienceAgent, and GeoPoliticsAgent

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Usage

Run the main script:
```bash
python -m pick_e.main
```

## Project Structure

```
pick_e/
├── agents/
│   ├── manager_agent.py
│   └── specialized_agents.py
├── crews/
│   └── specialized_crews.py
└── main.py
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
