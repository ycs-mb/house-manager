from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.models.database import get_db
from app.models import models, schemas
from datetime import datetime

router = APIRouter()

@router.get("/", response_model=List[schemas.Chore])
def list_chores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    chores = db.query(models.Chore).offset(skip).limit(limit).all()
    return chores

@router.post("/", response_model=schemas.Chore)
def create_chore(chore: schemas.ChoreCreate, db: Session = Depends(get_db)):
    # In a real app, we'd get household_id from the authenticated user
    # For local demo, we'll use a dummy ID or create one if none exists
    household = db.query(models.Household).first()
    if not household:
        household = models.Household(name="Default Household")
        db.add(household)
        db.commit()
        db.refresh(household)
    
    db_chore = models.Chore(**chore.model_dump(), household_id=household.id)
    db.add(db_chore)
    db.commit()
    db.refresh(db_chore)
    return db_chore

@router.patch("/{chore_id}", response_model=schemas.Chore)
def update_chore(chore_id: str, chore_update: schemas.ChoreUpdate, db: Session = Depends(get_db)):
    db_chore = db.query(models.Chore).filter(models.Chore.id == chore_id).first()
    if not db_chore:
        raise HTTPException(status_code=404, detail="Chore not found")
    
    update_data = chore_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_chore, key, value)
    
    db.commit()
    db.refresh(db_chore)
    return db_chore

@router.post("/{chore_id}/complete", response_model=schemas.Chore)
def complete_chore(chore_id: str, db: Session = Depends(get_db)):
    db_chore = db.query(models.Chore).filter(models.Chore.id == chore_id).first()
    if not db_chore:
        raise HTTPException(status_code=404, detail="Chore not found")
    
    db_chore.completed_at = datetime.utcnow()
    db.commit()
    db.refresh(db_chore)
    return db_chore
