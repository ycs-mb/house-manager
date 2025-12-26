from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.models.database import get_db
from app.models import models, schemas
from datetime import datetime

router = APIRouter()

@router.get("/", response_model=List[schemas.InventoryItem])
def list_inventory(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = db.query(models.InventoryItem).offset(skip).limit(limit).all()
    return items

@router.post("/", response_model=schemas.InventoryItem)
def add_inventory_item(item: schemas.InventoryItemCreate, db: Session = Depends(get_db)):
    household = db.query(models.Household).first()
    if not household:
        household = models.Household(name="Default Household")
        db.add(household)
        db.commit()
        db.refresh(household)
    
    db_item = models.InventoryItem(**item.model_dump(), household_id=household.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.patch("/{item_id}", response_model=schemas.InventoryItem)
def update_inventory_item(item_id: str, item_update: schemas.InventoryItemUpdate, db: Session = Depends(get_db)):
    db_item = db.query(models.InventoryItem).filter(models.InventoryItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    update_data = item_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)
    
    db_item.last_updated = datetime.utcnow()
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/low-stock", response_model=List[schemas.InventoryItem])
def get_low_stock(db: Session = Depends(get_db)):
    items = db.query(models.InventoryItem).filter(
        models.InventoryItem.quantity <= models.InventoryItem.low_stock_threshold
    ).all()
    return items
