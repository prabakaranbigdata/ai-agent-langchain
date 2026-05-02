# =========================================================
# SESSION 2: LLM AS DECISION MAKER (ReAct Style - Simple)
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
# 🤖 AGENT LOOP (LLM CONTROLS STEPS)
# =========================================================

def agent(user_input):
    print("\n===== SESSION 2 AGENT START =====\n")

    messages = [
        {"role": "system", "content": """
You are an AI agent that can plan trips.

You have access to tools:
1. travel_info → gives travel cost details
2. calculator → performs math calculations

Follow this format:

Thought: what you are thinking
Action: tool name (travel_info or calculator)
Action Input: input for the tool
Observation: result from tool

Repeat until final answer.

Rules:
- Use travel_info first
- Use calculator for total cost
- Always calculate before final answer
- Budget is ₹15000
"""},

        {"role": "user", "content": user_input}
    ]

    for step in range(5):  # limit steps to avoid infinite loop
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0,
            messages=messages
        )

        reply = response.choices[0].message.content
        print("\nLLM RESPONSE:\n", reply)

        messages.append({"role": "assistant", "content": reply})

        # =========================================================
        # 🔍 PARSE ACTION
        # =========================================================

        if "Final Answer" in reply:
            print("\n===== FINAL OUTPUT =====\n")
            print(reply)
            break

        if "Action:" in reply:
            try:
                action = re.search(r"Action:\s*(.*)", reply).group(1).strip()
                action_input = re.search(r"Action Input:\s*(.*)", reply).group(1).strip()
            except:
                print("⚠️ Could not parse action")
                break

            # =========================================================
            # ⚙️ EXECUTE TOOL
            # =========================================================

            if action == "travel_info":
                observation = travel_info()

            elif action == "calculator":
                observation = calculator(action_input)

            else:
                observation = "Unknown tool"

            print("\n🔧 TOOL EXECUTION:")
            print("Tool:", action)
            print("Input:", action_input)
            print("Output:", observation)

            # send observation back to LLM
            messages.append({
                "role": "user",
                "content": f"Observation: {observation}"
            })

# =========================================================
# ▶️ RUN
# =========================================================

if __name__ == "__main__":
    user_input = input("Enter your trip request: ")
    agent(user_input)