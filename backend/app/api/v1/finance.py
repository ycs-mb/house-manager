from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict
from app.models.database import get_db
from app.models import models, schemas
from datetime import datetime

router = APIRouter()

@router.get("/transactions", response_model=List[schemas.FinancialTransaction])
def list_transactions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    transactions = db.query(models.FinancialTransaction).order_by(models.FinancialTransaction.transaction_date.desc()).offset(skip).limit(limit).all()
    return transactions

@router.post("/transactions", response_model=schemas.FinancialTransaction)
def record_transaction(transaction: schemas.FinancialTransactionCreate, db: Session = Depends(get_db)):
    household = db.query(models.Household).first()
    if not household:
        household = models.Household(name="Default Household")
        db.add(household)
        db.commit()
        db.refresh(household)
    
    db_transaction = models.FinancialTransaction(**transaction.model_dump(), household_id=household.id)
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@router.get("/summary", response_model=schemas.FinanceSummary)
def get_finance_summary(db: Session = Depends(get_db)):
    transactions = db.query(models.FinancialTransaction).all()
    
    total_expenses = sum(float(t.amount) for t in transactions if t.is_expense)
    total_income = sum(float(t.amount) for t in transactions if not t.is_expense)
    
    category_breakdown = {}
    for t in transactions:
        cat = t.category or "Other"
        amount = float(t.amount)
        if t.is_expense:
            category_breakdown[cat] = category_breakdown.get(cat, 0) + amount
            
    return schemas.FinanceSummary(
        total_expenses=total_expenses,
        total_income=total_income,
        net_balance=total_income - total_expenses,
        category_breakdown=category_breakdown
    )
