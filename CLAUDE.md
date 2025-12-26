# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**PICK-E (Personal Intelligent Companion & Knowledge Ecosystem)** is a house manager application built on a multi-agent AI architecture using CrewAI. The system uses a central `ManagerAgent` that routes user requests to specialized crews based on keyword interpretation.

## Development Commands

### Quick Start (All Services)
```bash
./run_local.sh
```
This script starts both backend and frontend concurrently. Backend runs on port 8000, frontend on port 3000.

### Backend (FastAPI)
```bash
# Setup
cd backend
python -m venv venv
source venv/bin/activate  # or venv/bin/activate on Windows
pip install -r requirements.txt

# Run development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or from project root with proper PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd)/backend
./venv/bin/uvicorn app.main:app --reload
```

API documentation available at: http://localhost:8000/docs

### Frontend (Next.js)
```bash
cd frontend-web
npm install
npm run dev      # Development server on port 3000
npm run build    # Production build
npm start        # Production server
npm run lint     # Run ESLint
```

### Infrastructure (Docker)
```bash
docker-compose up    # Start Postgres and Redis
docker-compose down  # Stop services
```

Database credentials (docker-compose.yml):
- PostgreSQL: user/password/picke on port 5432
- Redis: port 6379

## Architecture

### Multi-Agent System (CrewAI)

The application uses a **crew-based architecture** where specialized agents are grouped into crews:

1. **ManagerAgent** (`backend/app/agents/manager_agent.py`)
   - Central orchestrator that routes requests to appropriate crews
   - Uses keyword-based interpretation (currently simple, intended for LLM-based routing in production)
   - Routes to three crew types: `knowledge`, `house`, `personal`

2. **Specialized Crews** (`backend/app/agents/specialized_crews.py`)
   - **PersonalManagementCrew**: Finance, Planner, Calendar agents
   - **KnowledgeCrew**: Idea, Reading, TechScience, GeoPolitics agents
   - **HouseManagementCrew**: Inventory, ChoreCoordinator agents

3. **Request Flow**:
   ```
   User Request → ManagerAgent._interpret_request()
               → Select appropriate Crew
               → Create CrewAI Task
               → crew.kickoff() (runs in ThreadPoolExecutor for async)
               → Return results
   ```

### API Structure

FastAPI application with versioned API routes (`/api/v1/`):
- `/api/v1/agents` - Agent interaction endpoints
- `/api/v1/chores` - Chore management
- `/api/v1/inventory` - Inventory tracking
- `/api/v1/finance` - Financial transactions

CORS is configured for local development (allow all origins).

### Database Models

SQLAlchemy models in `backend/app/models/models.py`:
- **Household**: Multi-tenant container with JSON settings
- **User**: Linked to household, includes role and preferences
- **Chore**: Task management with Trello integration support
- **InventoryItem**: Pantry/stock tracking with low stock thresholds
- **AgentTask**: Agent execution tracking
- **FinancialTransaction**: Expense/income tracking

All models use UUID primary keys (String 36).

### Configuration

Centralized in `backend/app/core/config.py` using Pydantic Settings:
- Loads from `.env` file (see `backend/.env.example`)
- Required environment variables:
  - `OPENAI_API_KEY` - For CrewAI agents
  - `DATABASE_URL` - Defaults to SQLite (`sqlite:///./picke.db`)
  - `REDIS_URL` - Defaults to `redis://localhost:6379/0`
  - `SECRET_KEY` - JWT authentication (change in production)
- Optional integrations: Trello, Notion, Google Cloud

### Frontend Architecture

Next.js 16 with App Router:
- **State Management**: Zustand
- **Styling**: Tailwind CSS 4
- **API Client**: `src/lib/api.ts` - helper for backend communication
- **React 19** with functional components

## Key Files

- `backend/app/main.py` - FastAPI app entry point, CORS config, router registration
- `backend/app/agents/manager_agent.py` - Request routing logic
- `backend/app/agents/specialized_crews.py` - Crew definitions
- `backend/app/agents/specialized_agents.py` - Individual agent implementations
- `backend/app/core/config.py` - Environment configuration
- `backend/app/models/models.py` - Database schema
- `backend/app/models/database.py` - SQLAlchemy setup
- `backend/app/models/init_db.py` - Database initialization
- `backend/app/models/seed.py` - Sample data seeding
- `run_local.sh` - Development startup script

## Important Notes

### CrewAI Integration
- Agents require `OPENAI_API_KEY` in environment
- `ManagerAgent.process_request()` runs crew.kickoff() in a ThreadPoolExecutor to maintain FastAPI async compatibility
- Crews are instantiated once at ManagerAgent initialization (stateful)
- Tasks are created dynamically per request and assigned to the first agent in the selected crew

### Database
- Default is SQLite (`picke.db` in project root) - ignored by git
- Production should use PostgreSQL via `DATABASE_URL` env var
- Use `backend/app/models/init_db.py` to initialize schema
- Use `backend/app/models/seed.py` to populate sample data

### Environment Setup
Always create `.env` file in `backend/` directory based on `.env.example` before running the backend.

### Legacy Files
Root-level files (`manager_agent.py`, `specialized_agents.py`, `specialized_crews.py`, `info_*.md/yaml`) are legacy/reference files. The active codebase is in `backend/app/`.
