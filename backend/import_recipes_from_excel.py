"""
Import recipes from Excel spreadsheet
"""
import sys
import os
import pandas as pd
from datetime import datetime

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(__file__))

from app.models.database import SessionLocal
from app.models import models

DEFAULT_HOUSEHOLD_ID = "default-household"

def extract_ingredients(recipe_name):
    """Extract basic ingredients from recipe name"""
    if pd.isna(recipe_name) or not recipe_name or recipe_name.strip() == '':
        return []

    # Split by common delimiters
    parts = str(recipe_name).replace('+', ',').replace(';', ',').split(',')
    ingredients = []

    for part in parts:
        part = part.strip()
        if part:
            ingredients.append({
                'name': part,
                'quantity': 1,
                'unit': 'serving'
            })

    return ingredients

def import_recipes_from_excel():
    """Import recipes from Excel file"""
    db = SessionLocal()

    try:
        # Read Excel file
        excel_path = '/Volumes/Mac-Partition/ycspb/Untitled spreadsheet.xlsx'
        df = pd.read_excel(excel_path)

        print(f"📊 Read {len(df)} rows from Excel file")

        # Delete all existing recipes
        deleted_recipes = db.query(models.Recipe).filter(
            models.Recipe.household_id == DEFAULT_HOUSEHOLD_ID
        ).delete()
        db.commit()
        print(f"🗑️  Deleted {deleted_recipes} existing recipes")

        # Track unique recipes by name and category
        unique_recipes = {}

        # Process each row
        for idx, row in df.iterrows():
            # Process each meal type
            meal_types = {
                'breakfast': row.get('Breakfast'),
                'lunch': row.get('Lunch'),
                'snack': row.get('Snacks'),
                'dinner': row.get('Dinner')
            }

            for meal_type, recipe_name in meal_types.items():
                # Skip if empty
                if pd.isna(recipe_name) or not recipe_name or str(recipe_name).strip() == '' or str(recipe_name).lower() == 'nan':
                    continue

                recipe_name = str(recipe_name).strip()

                # Create unique key for this recipe
                recipe_key = (recipe_name.lower(), meal_type)

                # Skip if already added
                if recipe_key in unique_recipes:
                    continue

                # Extract ingredients
                ingredients = extract_ingredients(recipe_name)

                # Create recipe
                recipe = models.Recipe(
                    household_id=DEFAULT_HOUSEHOLD_ID,
                    name=recipe_name,
                    description=f"{meal_type.capitalize()} recipe",
                    ingredients=ingredients,
                    instructions=f"Prepare {recipe_name}",
                    prep_time=15,
                    cook_time=30,
                    servings=4,
                    category=meal_type,
                    tags=[meal_type, "indian", "healthy"]
                )

                db.add(recipe)
                unique_recipes[recipe_key] = recipe

        db.commit()

        print(f"\n✅ Import completed successfully!")
        print(f"📝 Unique recipes created: {len(unique_recipes)}")

        # Show breakdown by category
        category_count = {}
        for (name, category) in unique_recipes.keys():
            category_count[category] = category_count.get(category, 0) + 1

        print(f"\n📊 Recipes by category:")
        for category, count in sorted(category_count.items()):
            print(f"   {category.capitalize()}: {count}")

        # Show total in database
        total_recipes = db.query(models.Recipe).filter(
            models.Recipe.household_id == DEFAULT_HOUSEHOLD_ID
        ).count()

        print(f"\n📚 Total recipes in database: {total_recipes}")

    except Exception as e:
        db.rollback()
        print(f"❌ Error importing data: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Starting recipe import from Excel...\n")
    import_recipes_from_excel()
