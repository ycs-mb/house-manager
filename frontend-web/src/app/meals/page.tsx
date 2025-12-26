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
  const [editingPlan, setEditingPlan] = useState<string | null>(null);
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
      // Start from December 27, 2025
      const startDate = new Date('2025-12-27T00:00:00');

      const response = await fetch('http://localhost:8000/api/v1/meals/meal-plans/generate-weekly', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          recipes: recipeIds,
          start_date: startDate.toISOString(),
          preferences: {}
        })
      });
      if (response.ok) {
        await loadMealPlans();
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

  const updateMealPlan = async (planId: string, recipeId: string) => {
    try {
      const response = await fetch(`http://localhost:8000/api/v1/meals/meal-plans/${planId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ recipe_id: recipeId })
      });
      if (response.ok) {
        await loadMealPlans();
        setEditingPlan(null);
      }
    } catch (error) {
      console.error('Error updating meal plan:', error);
    }
  };

  const deleteMealPlan = async (planId: string) => {
    if (!confirm('Are you sure you want to delete this meal plan?')) return;

    try {
      const response = await fetch(`http://localhost:8000/api/v1/meals/meal-plans/${planId}`, {
        method: 'DELETE'
      });
      if (response.ok) {
        await loadMealPlans();
      }
    } catch (error) {
      console.error('Error deleting meal plan:', error);
    }
  };

  const groupMealPlansByDate = () => {
    const grouped: { [key: string]: { breakfast?: MealPlan; lunch?: MealPlan; dinner?: MealPlan } } = {};

    mealPlans.forEach(plan => {
      const date = new Date(plan.planned_date).toISOString().split('T')[0];
      if (!grouped[date]) {
        grouped[date] = {};
      }
      grouped[date][plan.meal_type as 'breakfast' | 'lunch' | 'dinner'] = plan;
    });

    return grouped;
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
              <h2 style={{ fontSize: '1.5rem' }}>Weekly Meal Plan (Dec 27 - Jan 2, 2026)</h2>
              <button
                onClick={generateWeeklyPlan}
                style={{
                  padding: '0.75rem 1.5rem',
                  backgroundColor: '#6366f1',
                  border: 'none',
                  borderRadius: '8px',
                  color: 'white',
                  cursor: 'pointer',
                  fontWeight: 'bold'
                }}
              >
                Generate Weekly Plan
              </button>
            </div>

            {/* Calendar View */}
            <div style={{ display: 'grid', gap: '1rem' }}>
              {Object.entries(groupMealPlansByDate())
                .sort(([dateA], [dateB]) => dateA.localeCompare(dateB))
                .slice(0, 7)
                .map(([date, meals]) => {
                  const dateObj = new Date(date);
                  const dayName = dateObj.toLocaleDateString('en-US', { weekday: 'long' });
                  const dateStr = dateObj.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });

                  return (
                    <div key={date} style={{ backgroundColor: '#1a1a24', borderRadius: '12px', overflow: 'hidden' }}>
                      <div style={{ backgroundColor: '#6366f1', padding: '1rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <div>
                          <h3 style={{ fontSize: '1.2rem', fontWeight: 'bold' }}>{dayName}</h3>
                          <p style={{ fontSize: '0.875rem', opacity: 0.9 }}>{dateStr}</p>
                        </div>
                      </div>

                      <div style={{ padding: '1.5rem', display: 'grid', gap: '1rem' }}>
                        {['breakfast', 'lunch', 'dinner'].map(mealType => {
                          const plan = meals[mealType as 'breakfast' | 'lunch' | 'dinner'];

                          return (
                            <div key={mealType} style={{ display: 'flex', alignItems: 'center', gap: '1rem', paddingBottom: '1rem', borderBottom: mealType !== 'dinner' ? '1px solid #2a2a3a' : 'none' }}>
                              <div style={{ minWidth: '100px', fontWeight: 'bold', color: '#888', textTransform: 'capitalize' }}>
                                {mealType === 'breakfast' && '🌅'} {mealType === 'lunch' && '🌞'} {mealType === 'dinner' && '🌙'} {mealType}
                              </div>

                              {plan ? (
                                <div style={{ flex: 1, display: 'flex', alignItems: 'center', gap: '1rem' }}>
                                  {editingPlan === plan.id ? (
                                    <select
                                      value={plan.recipe_id}
                                      onChange={(e) => updateMealPlan(plan.id, e.target.value)}
                                      style={{ flex: 1, padding: '0.75rem', backgroundColor: '#2a2a3a', border: '1px solid #6366f1', borderRadius: '8px', color: 'white' }}
                                    >
                                      {recipes.map(recipe => (
                                        <option key={recipe.id} value={recipe.id}>{recipe.name}</option>
                                      ))}
                                    </select>
                                  ) : (
                                    <>
                                      <div style={{ flex: 1 }}>
                                        <p style={{ fontSize: '1rem', marginBottom: '0.25rem' }}>{plan.recipe?.name || 'No recipe'}</p>
                                        <p style={{ fontSize: '0.75rem', color: '#888' }}>
                                          {plan.recipe && `${plan.recipe.prep_time + plan.recipe.cook_time} min • ${plan.recipe.servings} servings`}
                                        </p>
                                      </div>
                                      <button
                                        onClick={() => setEditingPlan(plan.id)}
                                        style={{ padding: '0.5rem 1rem', backgroundColor: '#444', border: 'none', borderRadius: '6px', color: 'white', cursor: 'pointer', fontSize: '0.875rem' }}
                                      >
                                        Edit
                                      </button>
                                      <button
                                        onClick={() => deleteMealPlan(plan.id)}
                                        style={{ padding: '0.5rem 1rem', backgroundColor: '#ef4444', border: 'none', borderRadius: '6px', color: 'white', cursor: 'pointer', fontSize: '0.875rem' }}
                                      >
                                        Delete
                                      </button>
                                    </>
                                  )}
                                </div>
                              ) : (
                                <div style={{ flex: 1, color: '#666', fontStyle: 'italic' }}>No meal planned</div>
                              )}
                            </div>
                          );
                        })}
                      </div>
                    </div>
                  );
                })}
            </div>

            {mealPlans.length === 0 && (
              <div style={{ textAlign: 'center', padding: '4rem', color: '#888' }}>
                <p style={{ fontSize: '1.2rem', marginBottom: '1rem' }}>No meal plans yet</p>
                <p>Click "Generate Weekly Plan" to create your first meal plan!</p>
              </div>
            )}
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
