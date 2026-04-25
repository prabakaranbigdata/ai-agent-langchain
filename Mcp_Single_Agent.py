# =========================================================
# MCP-STYLE AGENT ARCHITECTURE (Single File)
# =========================================================

from langchain.chat_models import ChatOpenAI
import json
import os

# =========================================================
# 🧠 LLM
# =========================================================
llm = ChatOpenAI(
    model_name="gpt-4o-mini",
    temperature=0
)

# =========================================================
# 🔌 TOOLS (Decoupled)
# =========================================================
def calculator(expression):
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {str(e)}"

def knowledge(query):
    return llm.predict(query)

# =========================================================
# 📦 MCP TOOL REGISTRY
# =========================================================
class MCPToolRegistry:
    def __init__(self):
        self.tools = {}

    def register(self, name, func, description):
        self.tools[name] = {
            "func": func,
            "description": description
        }

    def get_tool(self, name):
        return self.tools.get(name)

# =========================================================
# 🔄 MCP EXECUTOR (CORE)
# =========================================================
class MCPExecutor:
    def __init__(self, registry):
        self.registry = registry

    def execute(self, tool_name, input_data):
        tool = self.registry.get_tool(tool_name)

        if not tool:
            return f"Tool '{tool_name}' not found"

        try:
            return tool["func"](input_data)
        except Exception as e:
            return f"Execution Error: {str(e)}"

# =========================================================
# 💾 MEMORY (Simple Long-Term)
# =========================================================
MEMORY_FILE = "memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return []

def save_memory(chat_history):
    with open(MEMORY_FILE, "w") as f:
        json.dump(chat_history, f, indent=2)

# =========================================================
# 🤖 AGENT (Decision Only)
# =========================================================
class Agent:
    def __init__(self, llm, mcp_executor, memory):
        self.llm = llm
        self.mcp = mcp_executor
        self.memory = memory

    def decide(self, user_input):
        prompt = f"""
You are an AI agent.

User Input: {user_input}

Available tools:
- Calculator: for math calculations
- Knowledge: for general knowledge

Decide the best tool and input.
Respond ONLY in JSON format:
{{
  "steps": [
    {{"tool": "Knowledge", "input": "extract the question part"}},
    {{"tool": "Calculator", "input": "extract the math expression"}}
  ]
}}
"""
        response = self.llm.predict(prompt)

        try:
            return json.loads(response)
        except:
            return {"tool": "Knowledge", "input": user_input}

    def run(self, user_input):
        print("\n--- USER INPUT ---")
        print(user_input)

        # Step 1: Decision
        decision = self.decide(user_input)

        steps = decision.get("steps", [])

        if not steps:
            print("⚠️ No steps found, fallback to Knowledge")
            steps = [{"tool": "Knowledge", "input": user_input}]

        final_outputs = []

        # Step 2: Execute each step via MCP
        for i, step in enumerate(steps, 1):
            tool_name = step.get("tool")
            tool_input = step.get("input")

            print(f"\n--- STEP {i} ---")
            print(f"Tool: {tool_name}")
            print(f"Input: {tool_input}")

            result = self.mcp.execute(tool_name, tool_input)

            print(f"Output: {result}")

            final_outputs.append(result)

        # Step 3: Combine results
        #final_response = "\n".join(final_outputs)
        final_context = "\n".join(final_outputs)

        final_prompt = f"""
User asked: {user_input}

Tool results:
{final_context}

IMPORTANT:
- Include ALL results from tools
- Do NOT ignore numeric or calculation results
- If there is a calculation, clearly mention the result

Give a clear, short final answer.
"""

        final_response = self.llm.predict(final_prompt)

        # Step 4: Save memory
        self.memory.append({
            "input": user_input,
            "steps": steps,
            "output": final_response
        })

        save_memory(self.memory)

        return final_response

# =========================================================
# ⚙️ SYSTEM SETUP
# =========================================================

# Load memory
memory_data = load_memory()

# Register tools
registry = MCPToolRegistry()
registry.register("Calculator", calculator, "Math calculations")
registry.register("Knowledge", knowledge, "General knowledge")

# MCP executor
mcp = MCPExecutor(registry)

# Agent
agent = Agent(llm, mcp, memory_data)

# =========================================================
# 🚀 RUN
# =========================================================
if __name__ == "__main__":
    while True:
        user_input = input("\nYou: ")

        if user_input.lower() in ["exit", "quit"]:
            print("Exiting...")
            break

        response = agent.run(user_input)
        print(f"AI: {response}")