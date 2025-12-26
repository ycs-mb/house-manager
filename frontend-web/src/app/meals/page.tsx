'use client';

import { useState, useEffect } from 'react';

interface Recipe {
  id: string;
  name: string;
  description: string;
  ingredients: Array<{ name: string; quantity: number; unit: string }>;
  instructions: string;
  prep_time: number;
  cook_time: number;
  servings: number;
  category: string;
  tags: string[];
}

interface MealPlan {
  id: string;
  recipe_id: string;
  meal_type: string;
  planned_date: string;
  status: string;
  recipe?: Recipe;
}

interface ShoppingListItem {
  id: string;
  name: string;
  quantity: number;
  unit: string;
  is_purchased: boolean;
  category: string;
}

export default function MealsPage() {
  const [activeTab, setActiveTab] = useState<'recipes' | 'planner' | 'shopping'>('recipes');
  const [recipes, setRecipes] = useState<Recipe[]>([]);
  const [mealPlans, setMealPlans] = useState<MealPlan[]>([]);
  const [shoppingList, setShoppingList] = useState<ShoppingListItem[]>([]);
  const [showRecipeForm, setShowRecipeForm] = useState(false);
  const [newRecipe, setNewRecipe] = useState({
    name: '',
    description: '',
    ingredients: [{ name: '', quantity: 1, unit: '' }],
    instructions: '',
    prep_time: 0,
    cook_time: 0,
    servings: 4,
    category: '',
    tags: []
  });

  useEffect(() => {
    loadRecipes();
    loadMealPlans();
    loadShoppingList();
  }, []);

  const loadRecipes = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/meals/recipes');
      const data = await response.json();
      setRecipes(data);
    } catch (error) {
      console.error('Error loading recipes:', error);
    }
  };

  const loadMealPlans = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/meals/meal-plans');
      const data = await response.json();
      setMealPlans(data);
    } catch (error) {
      console.error('Error loading meal plans:', error);
    }
  };

  const loadShoppingList = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/meals/shopping-list');
      const data = await response.json();
      setShoppingList(data);
    } catch (error) {
      console.error('Error loading shopping list:', error);
    }
  };

  const createRecipe = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/meals/recipes', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newRecipe)
      });
      if (response.ok) {
        loadRecipes();
        setShowRecipeForm(false);
        setNewRecipe({
          name: '',
          description: '',
          ingredients: [{ name: '', quantity: 1, unit: '' }],
          instructions: '',
          prep_time: 0,
          cook_time: 0,
          servings: 4,
          category: '',
          tags: []
        });
      }
    } catch (error) {
      console.error('Error creating recipe:', error);
    }
  };

  const generateWeeklyPlan = async () => {
    if (recipes.length === 0) {
      alert('Please add some recipes first!');
      return;
    }

    try {
      const recipeIds = recipes.map(r => r.id);
      const response = await fetch('http://localhost:8000/api/v1/meals/meal-plans/generate-weekly', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          recipes: recipeIds,
          start_date: new Date().toISOString(),
          preferences: {}
        })
      });
      if (response.ok) {
        loadMealPlans();
        alert('Weekly meal plan generated!');
      }
    } catch (error) {
      console.error('Error generating weekly plan:', error);
    }
  };

  const toggleShoppingItem = async (id: string, isPurchased: boolean) => {
    try {
      await fetch(`http://localhost:8000/api/v1/meals/shopping-list/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ is_purchased: !isPurchased })
      });
      loadShoppingList();
    } catch (error) {
      console.error('Error updating shopping item:', error);
    }
  };

  const addIngredient = () => {
    setNewRecipe({
      ...newRecipe,
      ingredients: [...newRecipe.ingredients, { name: '', quantity: 1, unit: '' }]
    });
  };

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#0a0a0f', color: 'white', padding: '2rem' }}>
      <div style={{ maxWidth: '1400px', margin: '0 auto' }}>
        <h1 style={{ fontSize: '2rem', fontWeight: 'bold', marginBottom: '2rem' }}>Meal Planner</h1>

        {/* Tabs */}
        <div style={{ display: 'flex', gap: '1rem', marginBottom: '2rem', borderBottom: '1px solid #333' }}>
          <button
            onClick={() => setActiveTab('recipes')}
            style={{
              padding: '0.75rem 1.5rem',
              backgroundColor: activeTab === 'recipes' ? '#6366f1' : 'transparent',
              border: 'none',
              color: 'white',
              cursor: 'pointer',
              borderRadius: '4px 4px 0 0'
            }}
          >
            Recipes
          </button>
          <button
            onClick={() => setActiveTab('planner')}
            style={{
              padding: '0.75rem 1.5rem',
              backgroundColor: activeTab === 'planner' ? '#6366f1' : 'transparent',
              border: 'none',
              color: 'white',
              cursor: 'pointer',
              borderRadius: '4px 4px 0 0'
            }}
          >
            Weekly Planner
          </button>
          <button
            onClick={() => setActiveTab('shopping')}
            style={{
              padding: '0.75rem 1.5rem',
              backgroundColor: activeTab === 'shopping' ? '#6366f1' : 'transparent',
              border: 'none',
              color: 'white',
              cursor: 'pointer',
              borderRadius: '4px 4px 0 0'
            }}
          >
            Shopping List
          </button>
        </div>

        {/* Recipes Tab */}
        {activeTab === 'recipes' && (
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '2rem' }}>
              <h2 style={{ fontSize: '1.5rem' }}>My Recipes</h2>
              <button
                onClick={() => setShowRecipeForm(!showRecipeForm)}
                style={{
                  padding: '0.75rem 1.5rem',
                  backgroundColor: '#6366f1',
                  border: 'none',
                  borderRadius: '8px',
                  color: 'white',
                  cursor: 'pointer'
                }}
              >
                {showRecipeForm ? 'Cancel' : 'Add Recipe'}
              </button>
            </div>

            {showRecipeForm && (
              <div style={{ backgroundColor: '#1a1a24', padding: '2rem', borderRadius: '12px', marginBottom: '2rem' }}>
                <h3 style={{ marginBottom: '1rem' }}>New Recipe</h3>
                <div style={{ display: 'grid', gap: '1rem' }}>
                  <input
                    type="text"
                    placeholder="Recipe Name"
                    value={newRecipe.name}
                    onChange={(e) => setNewRecipe({ ...newRecipe, name: e.target.value })}
                    style={{ padding: '0.75rem', backgroundColor: '#2a2a3a', border: '1px solid #444', borderRadius: '8px', color: 'white' }}
                  />
                  <textarea
                    placeholder="Description"
                    value={newRecipe.description}
                    onChange={(e) => setNewRecipe({ ...newRecipe, description: e.target.value })}
                    style={{ padding: '0.75rem', backgroundColor: '#2a2a3a', border: '1px solid #444', borderRadius: '8px', color: 'white', minHeight: '100px' }}
                  />

                  <div>
                    <h4 style={{ marginBottom: '0.5rem' }}>Ingredients</h4>
                    {newRecipe.ingredients.map((ing, idx) => (
                      <div key={idx} style={{ display: 'flex', gap: '0.5rem', marginBottom: '0.5rem' }}>
                        <input
                          type="text"
                          placeholder="Name"
                          value={ing.name}
                          onChange={(e) => {
                            const newIngs = [...newRecipe.ingredients];
                            newIngs[idx].name = e.target.value;
                            setNewRecipe({ ...newRecipe, ingredients: newIngs });
                          }}
                          style={{ flex: 2, padding: '0.5rem', backgroundColor: '#2a2a3a', border: '1px solid #444', borderRadius: '8px', color: 'white' }}
                        />
                        <input
                          type="number"
                          placeholder="Qty"
                          value={ing.quantity}
                          onChange={(e) => {
                            const newIngs = [...newRecipe.ingredients];
                            newIngs[idx].quantity = parseInt(e.target.value) || 0;
                            setNewRecipe({ ...newRecipe, ingredients: newIngs });
                          }}
                          style={{ flex: 1, padding: '0.5rem', backgroundColor: '#2a2a3a', border: '1px solid #444', borderRadius: '8px', color: 'white' }}
                        />
                        <input
                          type="text"
                          placeholder="Unit"
                          value={ing.unit}
                          onChange={(e) => {
                            const newIngs = [...newRecipe.ingredients];
                            newIngs[idx].unit = e.target.value;
                            setNewRecipe({ ...newRecipe, ingredients: newIngs });
                          }}
                          style={{ flex: 1, padding: '0.5rem', backgroundColor: '#2a2a3a', border: '1px solid #444', borderRadius: '8px', color: 'white' }}
                        />
                      </div>
                    ))}
                    <button
                      onClick={addIngredient}
                      style={{ padding: '0.5rem 1rem', backgroundColor: '#444', border: 'none', borderRadius: '8px', color: 'white', cursor: 'pointer' }}
                    >
                      + Add Ingredient
                    </button>
                  </div>

                  <textarea
                    placeholder="Instructions"
                    value={newRecipe.instructions}
                    onChange={(e) => setNewRecipe({ ...newRecipe, instructions: e.target.value })}
                    style={{ padding: '0.75rem', backgroundColor: '#2a2a3a', border: '1px solid #444', borderRadius: '8px', color: 'white', minHeight: '150px' }}
                  />

                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '1rem' }}>
                    <input
                      type="number"
                      placeholder="Prep Time (min)"
                      value={newRecipe.prep_time}
                      onChange={(e) => setNewRecipe({ ...newRecipe, prep_time: parseInt(e.target.value) || 0 })}
                      style={{ padding: '0.75rem', backgroundColor: '#2a2a3a', border: '1px solid #444', borderRadius: '8px', color: 'white' }}
                    />
                    <input
                      type="number"
                      placeholder="Cook Time (min)"
                      value={newRecipe.cook_time}
                      onChange={(e) => setNewRecipe({ ...newRecipe, cook_time: parseInt(e.target.value) || 0 })}
                      style={{ padding: '0.75rem', backgroundColor: '#2a2a3a', border: '1px solid #444', borderRadius: '8px', color: 'white' }}
                    />
                    <input
                      type="number"
                      placeholder="Servings"
                      value={newRecipe.servings}
                      onChange={(e) => setNewRecipe({ ...newRecipe, servings: parseInt(e.target.value) || 4 })}
                      style={{ padding: '0.75rem', backgroundColor: '#2a2a3a', border: '1px solid #444', borderRadius: '8px', color: 'white' }}
                    />
                  </div>

                  <button
                    onClick={createRecipe}
                    style={{ padding: '0.75rem', backgroundColor: '#6366f1', border: 'none', borderRadius: '8px', color: 'white', cursor: 'pointer', fontWeight: 'bold' }}
                  >
                    Save Recipe
                  </button>
                </div>
              </div>
            )}

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '1.5rem' }}>
              {recipes.map(recipe => (
                <div key={recipe.id} style={{ backgroundColor: '#1a1a24', padding: '1.5rem', borderRadius: '12px' }}>
                  <h3 style={{ fontSize: '1.25rem', marginBottom: '0.5rem' }}>{recipe.name}</h3>
                  <p style={{ color: '#888', fontSize: '0.875rem', marginBottom: '1rem' }}>{recipe.description}</p>
                  <div style={{ display: 'flex', gap: '1rem', fontSize: '0.875rem', color: '#aaa' }}>
                    <span>⏱️ {recipe.prep_time + recipe.cook_time} min</span>
                    <span>🍽️ {recipe.servings} servings</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Planner Tab */}
        {activeTab === 'planner' && (
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '2rem' }}>
              <h2 style={{ fontSize: '1.5rem' }}>Weekly Meal Plan</h2>
              <button
                onClick={generateWeeklyPlan}
                style={{
                  padding: '0.75rem 1.5rem',
                  backgroundColor: '#6366f1',
                  border: 'none',
                  borderRadius: '8px',
                  color: 'white',
                  cursor: 'pointer'
                }}
              >
                Generate Weekly Plan
              </button>
            </div>

            <div style={{ display: 'grid', gap: '1rem' }}>
              {mealPlans.map(plan => (
                <div key={plan.id} style={{ backgroundColor: '#1a1a24', padding: '1.5rem', borderRadius: '12px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <div>
                    <h3 style={{ fontSize: '1.1rem', marginBottom: '0.25rem' }}>{plan.recipe?.name || 'Unknown Recipe'}</h3>
                    <p style={{ color: '#888', fontSize: '0.875rem' }}>
                      {new Date(plan.planned_date).toLocaleDateString()} - {plan.meal_type}
                    </p>
                  </div>
                  <span style={{
                    padding: '0.5rem 1rem',
                    backgroundColor: plan.status === 'completed' ? '#10b981' : '#fbbf24',
                    borderRadius: '20px',
                    fontSize: '0.875rem'
                  }}>
                    {plan.status}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Shopping List Tab */}
        {activeTab === 'shopping' && (
          <div>
            <h2 style={{ fontSize: '1.5rem', marginBottom: '2rem' }}>Shopping List</h2>
            <div style={{ backgroundColor: '#1a1a24', padding: '2rem', borderRadius: '12px' }}>
              {shoppingList.length === 0 ? (
                <p style={{ color: '#888', textAlign: 'center' }}>No items in your shopping list</p>
              ) : (
                <div style={{ display: 'grid', gap: '0.75rem' }}>
                  {shoppingList.map(item => (
                    <div
                      key={item.id}
                      style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '1rem',
                        padding: '1rem',
                        backgroundColor: '#2a2a3a',
                        borderRadius: '8px'
                      }}
                    >
                      <input
                        type="checkbox"
                        checked={item.is_purchased}
                        onChange={() => toggleShoppingItem(item.id, item.is_purchased)}
                        style={{ width: '20px', height: '20px', cursor: 'pointer' }}
                      />
                      <div style={{ flex: 1 }}>
                        <span style={{
                          textDecoration: item.is_purchased ? 'line-through' : 'none',
                          color: item.is_purchased ? '#888' : 'white'
                        }}>
                          {item.name}
                        </span>
                        <span style={{ color: '#888', marginLeft: '0.5rem' }}>
                          - {item.quantity} {item.unit}
                        </span>
                      </div>
                      <span style={{ color: '#6366f1', fontSize: '0.875rem' }}>{item.category}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
