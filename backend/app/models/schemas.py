from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID

class HouseholdBase(BaseModel):
    name: str

class HouseholdCreate(HouseholdBase):
    pass

class Household(HouseholdBase):
    id: str
    created_at: datetime
    settings: Dict[str, Any]
    model_config = ConfigDict(from_attributes=True)

class ChoreBase(BaseModel):
    name: str
    description: Optional[str] = None
    frequency: Optional[str] = None
    points: int = 0
    due_date: Optional[datetime] = None

class ChoreCreate(ChoreBase):
    pass

class ChoreUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    frequency: Optional[str] = None
    assigned_to: Optional[str] = None
    due_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    points: Optional[int] = None

class Chore(ChoreBase):
    id: str
    household_id: str
    assigned_to: Optional[str] = None
    completed_at: Optional[datetime] = None
    trello_card_id: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class InventoryItemBase(BaseModel):
    name: str
    category: Optional[str] = None
    quantity: int = 0
    unit: Optional[str] = "pcs"
    expiration_date: Optional[datetime] = None
    low_stock_threshold: int = 1
    barcode: Optional[str] = None

class InventoryItemCreate(InventoryItemBase):
    pass

class InventoryItemUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    quantity: Optional[int] = None
    unit: Optional[str] = None
    expiration_date: Optional[datetime] = None
    low_stock_threshold: Optional[int] = None

class InventoryItem(InventoryItemBase):
    id: str
    household_id: str
    last_updated: datetime
    model_config = ConfigDict(from_attributes=True)

class AgentRequest(BaseModel):
    prompt: str
    context: Dict[str, Any] = {}

class AgentResponse(BaseModel):
    status: str
    messages: List[Dict[str, Any]]
    results: List[Dict[str, Any]]

class FinancialTransactionBase(BaseModel):
    amount: float
    category: Optional[str] = None
    description: Optional[str] = None
    is_expense: bool = True
    transaction_date: Optional[datetime] = None

class FinancialTransactionCreate(FinancialTransactionBase):
    pass

class FinancialTransaction(FinancialTransactionBase):
    id: str
    household_id: str
    recorded_by: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class FinanceSummary(BaseModel):
    total_expenses: float
    total_income: float
    net_balance: float
    category_breakdown: Dict[str, float]
