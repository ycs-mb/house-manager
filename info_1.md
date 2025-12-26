# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

PICK-E (Personal Intelligent Companion & Knowledge Ecosystem) is a multi-agent AI system built with CrewAI for personal productivity, financial management, knowledge capture, and insights gathering. The system uses a centralized ManagerAgent to orchestrate specialized agents and crews.

## Running the Application

```bash
# Activate virtual environment
source .venv/bin/activate

# Run the main application
python -m pick_e.main
```

## Development Setup

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

## Environment Variables

Create a `.env` file with:
```
OPENAI_API_KEY=your_openai_api_key_here
```

## Architecture

### Core Components

**ManagerAgent** (`pick_e/agents/manager_agent.py`)
- Central orchestrator that interprets requests and delegates to appropriate agents/crews
- Key methods (currently stubs):
  - `interpret_request()`: Analyzes incoming user requests
  - `prioritize_tasks()`: Evaluates and prioritizes tasks
  - `delegate_task()`: Assigns tasks to agents/crews
  - `monitor_progress()`: Tracks delegated tasks
  - `integrate_results()`: Combines results from multiple agents

**Specialized Agents** (`pick_e/agents/specialized_agents.py`)
- `FinanceAgent`: Personal finance management and investment analysis
- `PlannerAgent`: Daily planning and task management
- `IdeaAgent`: Knowledge capture and idea development
- `ReadingAgent`: Reading and learning optimization
- `TechScienceAgent`: Technology and science tracking
- `GeoPoliticsAgent`: Geopolitical analysis
- `CalendarAgent`: Calendar management

**Specialized Crews** (`pick_e/crews/specialized_crews.py`)
- `PersonalManagementCrew`: Combines FinanceAgent, PlannerAgent, and CalendarAgent
- `KnowledgeCrew`: Combines IdeaAgent, ReadingAgent, TechScienceAgent, and GeoPoliticsAgent
- Tasks are assigned dynamically by ManagerAgent (crews initialize with empty task lists)

### Request Flow

1. User request enters via `PICKE.process_request()`
2. ManagerAgent interprets the request using `interpret_request()`
3. ManagerAgent delegates to appropriate crew or agent via `delegate_task()`
4. Results are returned to the user

## Important Notes

- All agents inherit from `crewai.Agent` with `allow_delegation=True` and `verbose=True`
- All crews inherit from `crewai.Crew` with `verbose=True`
- The ManagerAgent's delegation logic is currently unimplemented (stub methods)
- No `__init__.py` files exist in the package directories (may affect imports)
- The system is designed for dynamic task assignment rather than pre-configured workflows
