SYSTEM_PROMPT = """
You are MealMind.

Rules:
- OUTPUT VALID JSON ONLY.
- Ingredient-only meals (no recipes, no instructions).
- Use cheap, repetitive foods unless variety is requested.
- Respect calorie, protein, and budget constraints.
- Stay under weekly budget.
"""

def build_user_prompt(data, prices):
    return f"""
User goals:
Calories/day: {data["calories"]}
Protein/day: {data["protein"]}
Meals/day: {data["meals"]}
Weekly budget (USD): {data["budget"]}

Allowed foods: {data["include"]}
Excluded foods: {data["exclude"]}

Price table (USD):
{prices}

Return JSON with:
- days[1..7]
- meals per day
- ingredient grams
- daily macro totals
- weekly shopping list
- weekly total cost
"""
