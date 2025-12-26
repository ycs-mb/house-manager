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

class RecipeBase(BaseModel):
    name: str
    description: Optional[str] = None
    ingredients: Optional[List[Dict[str, Any]]] = []
    instructions: Optional[str] = None
    prep_time: Optional[int] = None
    cook_time: Optional[int] = None
    servings: int = 4
    category: Optional[str] = None
    tags: Optional[List[str]] = []
    nutrition_info: Optional[Dict[str, Any]] = None

class RecipeCreate(RecipeBase):
    pass

class RecipeUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    ingredients: Optional[List[Dict[str, Any]]] = None
    instructions: Optional[str] = None
    prep_time: Optional[int] = None
    cook_time: Optional[int] = None
    servings: Optional[int] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    nutrition_info: Optional[Dict[str, Any]] = None

class Recipe(RecipeBase):
    id: str
    household_id: str
    created_at: datetime
    created_by: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class MealPlanBase(BaseModel):
    recipe_id: str
    meal_type: str
    planned_date: datetime
    notes: Optional[str] = None

class MealPlanCreate(MealPlanBase):
    pass

class MealPlanUpdate(BaseModel):
    recipe_id: Optional[str] = None
    meal_type: Optional[str] = None
    planned_date: Optional[datetime] = None
    status: Optional[str] = None
    notes: Optional[str] = None

class MealPlan(MealPlanBase):
    id: str
    household_id: str
    status: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class MealPlanWithRecipe(MealPlan):
    recipe: Optional[Recipe] = None
    model_config = ConfigDict(from_attributes=True)

class ShoppingListItemBase(BaseModel):
    name: str
    quantity: int = 1
    unit: Optional[str] = None
    category: Optional[str] = None
    priority: str = "normal"
    notes: Optional[str] = None
    added_from_recipe_id: Optional[str] = None

class ShoppingListItemCreate(ShoppingListItemBase):
    pass

class ShoppingListItemUpdate(BaseModel):
    name: Optional[str] = None
    quantity: Optional[int] = None
    unit: Optional[str] = None
    category: Optional[str] = None
    is_purchased: Optional[bool] = None
    priority: Optional[str] = None
    notes: Optional[str] = None

class ShoppingListItem(ShoppingListItemBase):
    id: str
    household_id: str
    is_purchased: bool
    created_at: datetime
    purchased_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)

class WeeklyMealPlanRequest(BaseModel):
    recipes: List[str]
    start_date: datetime
    preferences: Optional[Dict[str, Any]] = {}
