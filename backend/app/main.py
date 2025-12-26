from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import agents, chores, inventory, finance, meals

app = FastAPI(
    title="PICK-E House Manager API",
    description="Multi-agent AI system for house management and personal productivity",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For local development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to PICK-E House Manager API", "status": "running"}

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Include routers
app.include_router(agents.router, prefix="/api/v1/agents", tags=["Agents"])
app.include_router(chores.router, prefix="/api/v1/chores", tags=["Chores"])
app.include_router(inventory.router, prefix="/api/v1/inventory", tags=["Inventory"])
app.include_router(finance.router, prefix="/api/v1/finance", tags=["Finance"])
app.include_router(meals.router, prefix="/api/v1/meals", tags=["Meals"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
