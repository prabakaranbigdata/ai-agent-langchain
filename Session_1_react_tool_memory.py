# =========================================================
# SESSION 1 FINAL (NO LANGCHAIN - FULL CONTROL)
# =========================================================

import re
from openai import OpenAI

client = OpenAI()

# =========================================================
# 🧮 TOOL: Calculator
# =========================================================

def calculator(expression: str):
    try:
        if not re.match(r"^[0-9+\-*/(). ₹]+$", expression):
            return "ERROR: Only math expressions allowed"

        cleaned = re.sub(r"[^\d+\-*/(). ]", "", expression)
        result = eval(cleaned, {"__builtins__": None}, {})
        return str(result)

    except Exception as e:
        return f"ERROR: {str(e)}"

# =========================================================
# 🧳 TOOL: Travel Info
# =========================================================

def travel_info():
    return """
Train: 1500
Stay: 1000 per night
Food: 500 per day
Scooter: 400 per day
"""

# =========================================================
# 🤖 SIMPLE AGENT LOOP (ReAct Style)
# =========================================================

def agent(user_input):
    print("\n--- AGENT START ---\n")

    # Step 1: Get travel data
    print("Step 1: Fetching travel info...")
    info = travel_info()
    print(info)

    # Step 2: Build calculation
    print("\nStep 2: Creating cost expression...")

    # Hardcoded logic for teaching clarity
    stay = 1000 * 3
    food = 500 * 3
    travel = 1500
    scooter = 400 * 3

    expression = f"{stay} + {food} + {travel} + {scooter}"
    print("Expression:", expression)

    # Step 3: Calculate
    print("\nStep 3: Using calculator...")
    total = calculator(expression)
    print("Total Trip Cost:", total)
    if int(total) > 15000:
        print("⚠️ Over budget")
    else:
        print("✅ Within budget")

    # Step 4: Final Answer using LLM
    print("\nStep 4: Generating final answer...\n")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {"role": "system", "content": "You are a travel planner."},
            {"role": "user", "content": f"""
Plan a 3-day Goa trip.

Cost breakdown:
Stay: {stay}
Food: {food}
Travel: {travel}
Scooter: {scooter}

Total Cost: {total}

Budget: 15000

Give a final plan.
"""}
        ]
    )

    print(response.choices[0].message.content)

# =========================================================
# ▶️ RUN
# =========================================================

#agent("Plan a 3-day Goa trip under ₹15000")
user_input = input("Enter your trip request: ")
agent(user_input)