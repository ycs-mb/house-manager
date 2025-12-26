from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from app.models import models, schemas
from app.models.database import get_db

router = APIRouter()

# Default household ID for demo purposes
DEFAULT_HOUSEHOLD_ID = "default-household"

# Recipe endpoints
@router.post("/recipes", response_model=schemas.Recipe)
def create_recipe(recipe: schemas.RecipeCreate, db: Session = Depends(get_db)):
    db_recipe = models.Recipe(
        household_id=DEFAULT_HOUSEHOLD_ID,
        **recipe.model_dump()
    )
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

@router.get("/recipes", response_model=List[schemas.Recipe])
def get_recipes(
    skip: int = 0,
    limit: int = 100,
    category: str = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Recipe).filter(
        models.Recipe.household_id == DEFAULT_HOUSEHOLD_ID
    )
    if category:
        query = query.filter(models.Recipe.category == category)
    recipes = query.offset(skip).limit(limit).all()
    return recipes

@router.get("/recipes/{recipe_id}", response_model=schemas.Recipe)
def get_recipe(recipe_id: str, db: Session = Depends(get_db)):
    recipe = db.query(models.Recipe).filter(
        models.Recipe.id == recipe_id,
        models.Recipe.household_id == DEFAULT_HOUSEHOLD_ID
    ).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe

@router.put("/recipes/{recipe_id}", response_model=schemas.Recipe)
def update_recipe(
    recipe_id: str,
    recipe_update: schemas.RecipeUpdate,
    db: Session = Depends(get_db)
):
    db_recipe = db.query(models.Recipe).filter(
        models.Recipe.id == recipe_id,
        models.Recipe.household_id == DEFAULT_HOUSEHOLD_ID
    ).first()
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    update_data = recipe_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_recipe, field, value)

    db.commit()
    db.refresh(db_recipe)
    return db_recipe

@router.delete("/recipes/{recipe_id}")
def delete_recipe(recipe_id: str, db: Session = Depends(get_db)):
    db_recipe = db.query(models.Recipe).filter(
        models.Recipe.id == recipe_id,
        models.Recipe.household_id == DEFAULT_HOUSEHOLD_ID
    ).first()
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    db.delete(db_recipe)
    db.commit()
    return {"message": "Recipe deleted successfully"}

# Meal Plan endpoints
@router.post("/meal-plans", response_model=schemas.MealPlan)
def create_meal_plan(meal_plan: schemas.MealPlanCreate, db: Session = Depends(get_db)):
    # Verify recipe exists
    recipe = db.query(models.Recipe).filter(
        models.Recipe.id == meal_plan.recipe_id,
        models.Recipe.household_id == DEFAULT_HOUSEHOLD_ID
    ).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    db_meal_plan = models.MealPlan(
        household_id=DEFAULT_HOUSEHOLD_ID,
        **meal_plan.model_dump()
    )
    db.add(db_meal_plan)
    db.commit()
    db.refresh(db_meal_plan)
    return db_meal_plan

@router.get("/meal-plans", response_model=List[schemas.MealPlanWithRecipe])
def get_meal_plans(
    start_date: datetime = None,
    end_date: datetime = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.MealPlan).filter(
        models.MealPlan.household_id == DEFAULT_HOUSEHOLD_ID
    )

    if start_date:
        query = query.filter(models.MealPlan.planned_date >= start_date)
    if end_date:
        query = query.filter(models.MealPlan.planned_date <= end_date)

    meal_plans = query.order_by(models.MealPlan.planned_date).all()

    # Load recipes for each meal plan
    result = []
    for meal_plan in meal_plans:
        # Skip meal plans with null recipe_id
        if not meal_plan.recipe_id:
            continue

        recipe = db.query(models.Recipe).filter(
            models.Recipe.id == meal_plan.recipe_id
        ).first()
        meal_plan_dict = schemas.MealPlan.model_validate(meal_plan).model_dump()
        meal_plan_dict['recipe'] = schemas.Recipe.model_validate(recipe) if recipe else None
        result.append(schemas.MealPlanWithRecipe(**meal_plan_dict))

    return result

@router.get("/meal-plans/{meal_plan_id}", response_model=schemas.MealPlanWithRecipe)
def get_meal_plan(meal_plan_id: str, db: Session = Depends(get_db)):
    meal_plan = db.query(models.MealPlan).filter(
        models.MealPlan.id == meal_plan_id,
        models.MealPlan.household_id == DEFAULT_HOUSEHOLD_ID
    ).first()
    if not meal_plan:
        raise HTTPException(status_code=404, detail="Meal plan not found")

    recipe = db.query(models.Recipe).filter(
        models.Recipe.id == meal_plan.recipe_id
    ).first()

    meal_plan_dict = schemas.MealPlan.model_validate(meal_plan).model_dump()
    meal_plan_dict['recipe'] = schemas.Recipe.model_validate(recipe) if recipe else None

    return schemas.MealPlanWithRecipe(**meal_plan_dict)

@router.put("/meal-plans/{meal_plan_id}", response_model=schemas.MealPlan)
def update_meal_plan(
    meal_plan_id: str,
    meal_plan_update: schemas.MealPlanUpdate,
    db: Session = Depends(get_db)
):
    db_meal_plan = db.query(models.MealPlan).filter(
        models.MealPlan.id == meal_plan_id,
        models.MealPlan.household_id == DEFAULT_HOUSEHOLD_ID
    ).first()
    if not db_meal_plan:
        raise HTTPException(status_code=404, detail="Meal plan not found")

    update_data = meal_plan_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_meal_plan, field, value)

    db.commit()
    db.refresh(db_meal_plan)
    return db_meal_plan

@router.delete("/meal-plans/{meal_plan_id}")
def delete_meal_plan(meal_plan_id: str, db: Session = Depends(get_db)):
    db_meal_plan = db.query(models.MealPlan).filter(
        models.MealPlan.id == meal_plan_id,
        models.MealPlan.household_id == DEFAULT_HOUSEHOLD_ID
    ).first()
    if not db_meal_plan:
        raise HTTPException(status_code=404, detail="Meal plan not found")

    db.delete(db_meal_plan)
    db.commit()
    return {"message": "Meal plan deleted successfully"}

# Weekly meal plan generation
@router.post("/meal-plans/generate-weekly")
def generate_weekly_meal_plan(
    request: schemas.WeeklyMealPlanRequest,
    db: Session = Depends(get_db)
):
    meal_types = ["breakfast", "lunch", "snack", "dinner"]
    created_plans = []

    # Get all available recipes and categorize by meal type
    all_recipes = db.query(models.Recipe).filter(
        models.Recipe.household_id == DEFAULT_HOUSEHOLD_ID
    ).all()

    # Group recipes by category for better variety
    recipes_by_category = {
        "breakfast": [r for r in all_recipes if r.category == "breakfast"],
        "lunch": [r for r in all_recipes if r.category == "lunch"],
        "snack": [r for r in all_recipes if r.category == "snack"],
        "dinner": [r for r in all_recipes if r.category == "dinner"],
    }

    # Track used recipes to avoid repetition
    used_recipes = {mt: set() for mt in meal_types}

    # Generate meal plans for 7 days
    for day in range(7):
        current_date = request.start_date + timedelta(days=day)

        for meal_type in meal_types:
            # Get available recipes for this meal type
            available_recipes = recipes_by_category.get(meal_type, [])

            # If no category-specific recipes, use any recipe
            if not available_recipes:
                available_recipes = all_recipes

            # Filter out already used recipes for variety
            unused_recipes = [r for r in available_recipes if r.id not in used_recipes[meal_type]]

            # If all recipes used, reset the used set for this meal type
            if not unused_recipes:
                used_recipes[meal_type] = set()
                unused_recipes = available_recipes

            if not unused_recipes:
                continue

            # Select recipe (use index-based selection with variety)
            recipe_index = day % len(unused_recipes)
            recipe = unused_recipes[recipe_index]
            used_recipes[meal_type].add(recipe.id)

            # Create meal plan with appropriate hour
            hour = 8 if meal_type == "breakfast" else 12 if meal_type == "lunch" else 15 if meal_type == "snack" else 18
            meal_plan = models.MealPlan(
                household_id=DEFAULT_HOUSEHOLD_ID,
                recipe_id=recipe.id,
                meal_type=meal_type,
                planned_date=current_date.replace(hour=hour, minute=0, second=0)
            )
            db.add(meal_plan)
            created_plans.append(meal_plan)

    db.commit()
    for plan in created_plans:
        db.refresh(plan)

    return {
        "message": f"Generated {len(created_plans)} meal plans",
        "plans": [schemas.MealPlan.model_validate(p) for p in created_plans]
    }

# Shopping List endpoints
@router.get("/shopping-list", response_model=List[schemas.ShoppingListItem])
def get_shopping_list(
    include_purchased: bool = False,
    db: Session = Depends(get_db)
):
    query = db.query(models.ShoppingListItem).filter(
        models.ShoppingListItem.household_id == DEFAULT_HOUSEHOLD_ID
    )

    if not include_purchased:
        query = query.filter(models.ShoppingListItem.is_purchased == False)

    items = query.order_by(models.ShoppingListItem.created_at.desc()).all()
    return items

@router.post("/shopping-list", response_model=schemas.ShoppingListItem)
def add_shopping_list_item(
    item: schemas.ShoppingListItemCreate,
    db: Session = Depends(get_db)
):
    db_item = models.ShoppingListItem(
        household_id=DEFAULT_HOUSEHOLD_ID,
        **item.model_dump()
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.put("/shopping-list/{item_id}", response_model=schemas.ShoppingListItem)
def update_shopping_list_item(
    item_id: str,
    item_update: schemas.ShoppingListItemUpdate,
    db: Session = Depends(get_db)
):
    db_item = db.query(models.ShoppingListItem).filter(
        models.ShoppingListItem.id == item_id,
        models.ShoppingListItem.household_id == DEFAULT_HOUSEHOLD_ID
    ).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Shopping list item not found")

    update_data = item_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_item, field, value)

    if update_data.get('is_purchased') and not db_item.purchased_at:
        db_item.purchased_at = datetime.utcnow()

    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/shopping-list/{item_id}")
def delete_shopping_list_item(item_id: str, db: Session = Depends(get_db)):
    db_item = db.query(models.ShoppingListItem).filter(
        models.ShoppingListItem.id == item_id,
        models.ShoppingListItem.household_id == DEFAULT_HOUSEHOLD_ID
    ).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Shopping list item not found")

    db.delete(db_item)
    db.commit()
    return {"message": "Shopping list item deleted successfully"}

@router.post("/shopping-list/from-meal-plan/{meal_plan_id}")
def generate_shopping_list_from_meal_plan(
    meal_plan_id: str,
    db: Session = Depends(get_db)
):
    meal_plan = db.query(models.MealPlan).filter(
        models.MealPlan.id == meal_plan_id,
        models.MealPlan.household_id == DEFAULT_HOUSEHOLD_ID
    ).first()
    if not meal_plan:
        raise HTTPException(status_code=404, detail="Meal plan not found")

    recipe = db.query(models.Recipe).filter(
        models.Recipe.id == meal_plan.recipe_id
    ).first()
    if not recipe or not recipe.ingredients:
        raise HTTPException(status_code=404, detail="Recipe or ingredients not found")

    created_items = []
    for ingredient in recipe.ingredients:
        item = models.ShoppingListItem(
            household_id=DEFAULT_HOUSEHOLD_ID,
            name=ingredient.get('name', ''),
            quantity=ingredient.get('quantity', 1),
            unit=ingredient.get('unit', ''),
            category=ingredient.get('category', 'Other'),
            added_from_recipe_id=recipe.id
        )
        db.add(item)
        created_items.append(item)

    db.commit()
    for item in created_items:
        db.refresh(item)

    return {
        "message": f"Added {len(created_items)} items to shopping list",
        "items": [schemas.ShoppingListItem.model_validate(i) for i in created_items]
    }
