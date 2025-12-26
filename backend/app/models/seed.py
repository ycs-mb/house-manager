from sqlalchemy.orm import Session
from app.models.database import SessionLocal, engine
from app.models import models
from datetime import datetime, timedelta

def seed_db():
    db = SessionLocal()
    try:
        # Create Household
        household = models.Household(name="YCS Household")
        db.add(household)
        db.commit()
        db.refresh(household)

        # Create User
        user = models.User(
            household_id=household.id,
            email="user@example.com",
            name="Assistant",
            hashed_password="hashed_password", # dummy
            role="admin"
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        # Create Chores
        chores = [
            models.Chore(household_id=household.id, name="Clean Kitchen", frequency="daily", points=10),
            models.Chore(household_id=household.id, name="Vacuum Living Room", frequency="weekly", points=20),
            models.Chore(household_id=household.id, name="Wash Bathroom", frequency="weekly", points=50, due_date=datetime.utcnow() - timedelta(days=1)),
            models.Chore(household_id=household.id, name="Grocery Shopping", frequency="weekly", points=30),
        ]
        db.add_all(chores)

        # Create Inventory
        items = [
            models.InventoryItem(household_id=household.id, name="Milk", category="Dairy", quantity=0, unit="L", low_stock_threshold=1),
            models.InventoryItem(household_id=household.id, name="Eggs", category="Dairy", quantity=2, unit="pcs", low_stock_threshold=6),
            models.InventoryItem(household_id=household.id, name="Bread", category="Bakery", quantity=1, unit="pcs", low_stock_threshold=1),
        ]
        db.add_all(items)

        # Create Transactions
        transactions = [
            models.FinancialTransaction(household_id=household.id, amount=1200.00, category="Salary", description="Initial Balance", is_expense=False),
            models.FinancialTransaction(household_id=household.id, amount=42.50, category="Groceries", description="Weekly veggies", is_expense=True),
        ]
        db.add_all(transactions)

        db.commit()
        print("Database seeded successfully!")
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()
