from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, DECIMAL, Boolean, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from .database import Base

class Household(Base):
    __tablename__ = "households"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    settings = Column(JSON, default={})
    
    users = relationship("User", back_populates="household")
    chores = relationship("Chore", back_populates="household")
    inventory_items = relationship("InventoryItem", back_populates="household")

class User(Base):
    __tablename__ = "users"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    household_id = Column(String(36), ForeignKey("households.id"))
    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255))
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), default="member")
    preferences = Column(JSON, default={})
    
    household = relationship("Household", back_populates="users")

class Chore(Base):
    __tablename__ = "chores"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    household_id = Column(String(36), ForeignKey("households.id"))
    name = Column(String(255), nullable=False)
    description = Column(Text)
    frequency = Column(String(50))
    assigned_to = Column(String(36), ForeignKey("users.id"))
    due_date = Column(DateTime)
    completed_at = Column(DateTime)
    trello_card_id = Column(String(255))
    points = Column(Integer, default=0)
    
    household = relationship("Household", back_populates="chores")

class InventoryItem(Base):
    __tablename__ = "inventory_items"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    household_id = Column(String(36), ForeignKey("households.id"))
    name = Column(String(255), nullable=False)
    category = Column(String(100))
    quantity = Column(Integer, default=0)
    unit = Column(String(50))
    expiration_date = Column(DateTime)
    low_stock_threshold = Column(Integer, default=1)
    barcode = Column(String(255))
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    household = relationship("Household", back_populates="inventory_items")

class AgentTask(Base):
    __tablename__ = "agent_tasks"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    agent_name = Column(String(100))
    task_type = Column(String(100))
    status = Column(String(50), default="pending")
    input_data = Column(JSON)
    output_data = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    error_message = Column(Text)

class FinancialTransaction(Base):
    __tablename__ = "financial_transactions"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    household_id = Column(String(36), ForeignKey("households.id"))
    amount = Column(DECIMAL(10, 2), nullable=False)
    category = Column(String(100))
    description = Column(String(255))
    transaction_date = Column(DateTime, default=datetime.utcnow)
    recorded_by = Column(String(36), ForeignKey("users.id"))
    is_expense = Column(Boolean, default=True)
