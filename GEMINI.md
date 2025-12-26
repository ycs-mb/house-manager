# PICK-E House Manager Project Context

## Project Overview
**PICK-E** (Personal Intelligent Companion & Knowledge Ecosystem) is an autonomous digital ecosystem designed for personal productivity, house management, and knowledge organization. It utilizes a multi-agent system (CrewAI) to handle tasks ranging from financial planning and daily scheduling to household chores and knowledge capture.

## Tech Stack

### Backend
*   **Language:** Python 3.13
*   **Framework:** FastAPI
*   **AI Framework:** CrewAI
*   **Database:** SQLAlchemy (SQLite/Postgres), Redis
*   **Authentication:** Python-Jose (JWT), Passlib (Bcrypt)
*   **Key Libraries:** Pydantic, Uvicorn, Python-Multipart

### Frontend (Web)
*   **Framework:** Next.js 16 (React 19)
*   **Styling:** Tailwind CSS 4
*   **Language:** TypeScript
*   **State Management:** Zustand
*   **Visualization:** Recharts
*   **Icons:** Lucide-React

### Infrastructure
*   **Containerization:** Docker & Docker Compose
*   **Services:** Postgres (v15), Redis (v7)

## Project Structure

```
/
├── backend/                # Main Python/FastAPI Application
│   ├── app/
│   │   ├── agents/         # CrewAI Agent definitions & Crews
│   │   ├── api/            # API Route endpoints (v1)
│   │   ├── core/           # Configuration & Settings
│   │   ├── models/         # Database models & Schemas
│   │   ├── services/       # Business logic services
│   │   └── main.py         # App Entry point
│   └── requirements.txt    # Backend dependencies
├── frontend-web/           # Next.js Web Application
│   ├── src/                # Source code
│   ├── public/             # Static assets
│   └── package.json        # Frontend dependencies
├── docker-compose.yml      # Infrastructure orchestration
└── manager_agent.py        # (Legacy/Standalone) Agent script
```

## Setup & Development

### Backend
1.  Navigate to `backend/`.
2.  Create virtual environment: `python -m venv venv`
3.  Activate: `source venv/bin/activate`
4.  Install: `pip install -r requirements.txt`
5.  Run: `uvicorn app.main:app --reload`
    *   API runs at: `http://localhost:8000`
    *   Docs: `http://localhost:8000/docs`

### Frontend
1.  Navigate to `frontend-web/`.
2.  Install: `npm install`
3.  Run: `npm run dev`
    *   App runs at: `http://localhost:3000`

### Docker (Full Stack/Infra)
*   Run `docker-compose up` to start the database and redis services.

## Development Conventions

*   **Python/Backend:**
    *   Use Pydantic models for data validation and schema definition.
    *   Follow `backend/app/` module structure.
    *   Configuration is centralized in `backend/app/core/config.py`.
    *   Agents are implemented in `backend/app/agents/` and orchestrated via `ManagerAgent`.
*   **Frontend:**
    *   Use Next.js App Router.
    *   Use Functional Components with Hooks.
    *   Style with Tailwind CSS utility classes.
*   **AI/Agents:**
    *   Agents are organized into "Crews" (e.g., `PersonalManagementCrew`, `KnowledgeCrew`).
    *   The `ManagerAgent` acts as the router/orchestrator for requests.

## Key Files
*   `backend/app/main.py`: Backend entry point.
*   `backend/app/core/config.py`: Environment and app configuration.
*   `backend/app/agents/manager_agent.py`: Main logic for routing user requests to specific crews.
*   `frontend-web/package.json`: Frontend dependency definitions.
*   `docker-compose.yml`: Service definitions.
