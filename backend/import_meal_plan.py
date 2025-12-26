"""
Import meal plan data from CSV format into the database
"""
import sys
import os
from datetime import datetime

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(__file__))

from app.models.database import SessionLocal
from app.models import models
import uuid

# Meal plan data
meal_data = """Mon,November 10, 2025,"Ragi dosa and chutney sambhar","Palak Dal + Cabbage carrot and peas","Tomato red capsicum soup, Paneer Gravy"
Tue,November 11, 2025,"Vermicelli","Soya nuggets gravy","Kundru, Mix Dal"
Wed,November 12, 2025,"Suji Uttapam","Sweet potato","Jeera lauki"
Thur,November 13, 2025,"Moong Dal Chilla","Lasooni Palak corn",""
Fri,November 14, 2025,"","Paneer Gravy",""
Sat,November 15, 2025,"","",""
Sunday,November 2, 2025,"Appe","Paneer + Parantha","Pineapple Coconut Curry with Idiappam"
Monday,November 3, 2025,"Semiyan","Mogar Dal + Amaranthus Roti + Cucumber Turai + Roti","Tomato Soup; Apple, Roasted Channa with onion and chutney"
Tuesday,November 4, 2025,"Gobhi Parantha","Palak Dal + Lauki","Parwal + Mix Dal"
Wednesday,November 5, 2025,"Sweet Potato","Pumpkin, Broccoli soup",""
Thursday,November 6, 2025,"","Arbi + Dal","Kheksa"
Friday,November 7, 2025,"Black Channa","Aloo Gobhi Gravy",""
Saturday,November 8, 2025,"","",""
Sunday,September 26, 2021,"Besan Chilla + Paneer + Veggies","Paneer + Veggies + Rice + curd","Idly + sambhar; Almond"
Monday,September 27, 2021,"Poha + Veggies + Peanuts","Soya + Veggies + Rice + curd","Rice + Palak + Paneer; Almond"
Tuesday,September 21, 2019,"Moong Dal Chilla + Veggies + Cheese","Rajma + Rice + Veggies + Curd","Paneer + Veggies + Rice; Almond"
Wednesday,July 10, 2019,"Upma + Veggies + Peanuts","Soya Salad + Rice + Curd","Paneer + Rice + Veggie; Almond"
Thursday,July 11, 2019,"Besan Chilla + Paneer + Veggies","Paneer + Veggies + Rice + curd","Idly + sambhar; Almond"
Friday,July 12, 2019,"Moong Dal Chilla + Veggies + Cheese","Chole + Rice + Veggies + Curd","Paneer + Veggies + Rice; Almond"
Saturday,July 13, 2019,"","",""
"""

DEFAULT_HOUSEHOLD_ID = "default-household"

def parse_date(date_str):
    """Parse date string to datetime object"""
    try:
        date_str = date_str.strip()
        # Try different date formats
        for fmt in ["%B %d, %Y", "%B %d,%Y", "%B %d %Y"]:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue

        # If no year provided, assume current year
        for fmt in ["%B %d", "%B %d,"]:
            try:
                dt = datetime.strptime(date_str, fmt)
                return dt.replace(year=2025)  # Default to 2025
            except ValueError:
                continue

        print(f"Could not parse date: '{date_str}'")
        return None
    except Exception as e:
        print(f"Error parsing date '{date_str}': {e}")
        return None

def extract_ingredients(recipe_name):
    """Extract basic ingredients from recipe name"""
    # Split by common delimiters
    parts = recipe_name.replace('+', ',').replace(';', ',').split(',')
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

def get_or_create_recipe(db, recipe_name, meal_type):
    """Get existing recipe or create new one"""
    # Check if recipe already exists
    existing = db.query(models.Recipe).filter(
        models.Recipe.name == recipe_name,
        models.Recipe.household_id == DEFAULT_HOUSEHOLD_ID
    ).first()

    if existing:
        return existing

    # Create new recipe
    ingredients = extract_ingredients(recipe_name)

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
    db.flush()
    return recipe

def import_meal_plan():
    """Import meal plan data into database"""
    db = SessionLocal()

    try:
        lines = meal_data.strip().split('\n')
        recipes_created = 0
        meal_plans_created = 0

        for line in lines:
            # Parse CSV line (handle quoted fields)
            parts = []
            current = ""
            in_quotes = False

            for char in line:
                if char == '"':
                    in_quotes = not in_quotes
                elif char == ',' and not in_quotes:
                    parts.append(current.strip())
                    current = ""
                else:
                    current += char
            parts.append(current.strip())

            if len(parts) < 5:
                continue

            day_name, date_str, breakfast, lunch, dinner = parts[:5]

            # Parse date
            parsed_date = parse_date(date_str)
            if not parsed_date:
                print(f"Skipping invalid date: {date_str}")
                continue

            # Process each meal type
            meals = {
                'breakfast': (breakfast.strip('"').strip(), 8),
                'lunch': (lunch.strip('"').strip(), 12),
                'dinner': (dinner.strip('"').strip(), 18)
            }

            for meal_type, (recipe_name, hour) in meals.items():
                if not recipe_name:
                    continue

                # Get or create recipe
                recipe = get_or_create_recipe(db, recipe_name, meal_type)
                if not recipe.id:
                    recipes_created += 1

                # Create meal plan
                meal_plan = models.MealPlan(
                    household_id=DEFAULT_HOUSEHOLD_ID,
                    recipe_id=recipe.id,
                    meal_type=meal_type,
                    planned_date=parsed_date.replace(hour=hour, minute=0, second=0),
                    status='planned',
                    notes=f"Imported from meal plan - {day_name}"
                )

                db.add(meal_plan)
                meal_plans_created += 1

        db.commit()
        print(f"\n✅ Import completed successfully!")
        print(f"📝 Recipes created: {recipes_created}")
        print(f"📅 Meal plans created: {meal_plans_created}")

        # Show summary
        total_recipes = db.query(models.Recipe).filter(
            models.Recipe.household_id == DEFAULT_HOUSEHOLD_ID
        ).count()
        total_meal_plans = db.query(models.MealPlan).filter(
            models.MealPlan.household_id == DEFAULT_HOUSEHOLD_ID
        ).count()

        print(f"\n📊 Database Summary:")
        print(f"   Total recipes: {total_recipes}")
        print(f"   Total meal plans: {total_meal_plans}")

    except Exception as e:
        db.rollback()
        print(f"❌ Error importing data: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Starting meal plan import...\n")
    import_meal_plan()
