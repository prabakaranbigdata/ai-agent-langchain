# =========================================================
# SESSION 3: MULTI-AGENT SYSTEM (NO FRAMEWORK)
# =========================================================

from openai import OpenAI
import re

client = OpenAI()

# =========================================================
# 🧮 TOOL: Calculator
# =========================================================

def calculator(expression: str):
    try:
        cleaned = re.sub(r"[^\d+\-*/(). ]", "", expression)
        result = eval(cleaned, {"__builtins__": None}, {})
        return str(result)
    except:
        return "ERROR"

# =========================================================
# 🧠 AGENT 1: PLANNER
# =========================================================

def planner_agent(user_input):
    print("\n🧠 PLANNER AGENT THINKING...\n")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {"role": "system", "content": """
You are a travel planner.

Create a simple 3-day Goa trip plan including:
- Travel
- Stay
- Food
- Activities

Keep it realistic and budget-friendly.
"""},
            {"role": "user", "content": user_input}
        ]
    )

    plan = response.choices[0].message.content
    print("📋 PLAN:\n", plan)
    return plan

# =========================================================
# 💰 AGENT 2: BUDGET ANALYZER
# =========================================================

def budget_agent(plan):
    print("\n💰 BUDGET AGENT ANALYZING...\n")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {"role": "system", "content": """
You are a budget analyst.

Estimate total cost using:
- Train: 1500
- Stay: 1000 per night
- Food: 500 per day
- Scooter: 400 per day

Give:
1. Cost breakdown
2. Total cost
3. Whether within ₹15000
"""},
            {"role": "user", "content": plan}
        ]
    )

    budget = response.choices[0].message.content
    print("💵 COST ANALYSIS:\n", budget)
    return budget

# =========================================================
# ✅ AGENT 3: REVIEWER
# =========================================================

def reviewer_agent(plan, budget):
    print("\n✅ REVIEWER AGENT VALIDATING...\n")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {"role": "system", "content": """
You are a reviewer.

Check:
- Is the plan realistic?
- Is it within ₹15000?

If over budget:
- Suggest improvements
- Optimize the plan

Give final improved plan.
"""},
            {"role": "user", "content": f"""
Plan:
{plan}

Budget Analysis:
{budget}
"""}
        ]
    )

    final = response.choices[0].message.content
    print("🎯 FINAL OUTPUT:\n", final)
    return final

# =========================================================
# 🔁 ORCHESTRATOR
# =========================================================

def multi_agent_system(user_input):
    print("\n===== MULTI-AGENT SYSTEM START =====\n")

    # Step 1: Planner
    plan = planner_agent(user_input)

    # Step 2: Budget
    budget = budget_agent(plan)

    # Step 3: Reviewer
    final = reviewer_agent(plan, budget)

    return final

# =========================================================
# ▶️ RUN
# =========================================================

if __name__ == "__main__":
    user_input = input("Enter your trip request: ")
    multi_agent_system(user_input)