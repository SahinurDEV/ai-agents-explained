# Module 02 Sample Solution: Design an Agent on One Page

**Example: Meal-planning agent**
1. Goal: plan 7 dinners within a budget, using what is already in the fridge.
2. Model: any chat LLM. Instructions: budget, dietary rules, ask before buying. Tools: `pantry_list()`, `recipe_search(ingredients)`, `price_lookup(item)`, `add_to_cart(item)` (needs approval). Memory: preferences ("no beef", "likes spicy"). Knowledge: family recipes document.
3. Loop: (a) think: need pantry -> call `pantry_list` -> observe rice, eggs, spinach; (b) think: find recipes -> `recipe_search` -> 12 options; (c) think: check cost of missing items -> `price_lookup` -> total 18 USD; (d) answer: plan + shopping list, ask approval to add to cart.
4. Autonomy: act-with-approval, because buying spends money.
5. A fixed workflow could do pantry -> recipes, but choosing and re-planning around prices and preferences benefits from an agent. If the steps never vary, use a workflow - it is cheaper and more predictable.
