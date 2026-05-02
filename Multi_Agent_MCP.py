# =========================================================
# MULTI-AGENT AI + MCP ARCHITECTURE (Dynamic Version)
# Beginner Friendly Version for Somethingtalk1
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
# 🔌 TOOLS
# =========================================================

def calculator(expression):
    """
    Simple calculator tool
    """
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Calculator Error: {str(e)}"


def knowledge(query):
    """
    Knowledge tool using LLM
    """
    try:
        return llm.predict(query)
    except Exception as e:
        return f"Knowledge Error: {str(e)}"


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
# 🔄 MCP EXECUTOR
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
# 💾 SIMPLE MEMORY
# =========================================================

MEMORY_FILE = "multi_agent_memory.json"


def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return []


def save_memory(chat_history):
    with open(MEMORY_FILE, "w") as f:
        json.dump(chat_history, f, indent=2)


# =========================================================
# 🤖 AGENT 1 → RESEARCH AGENT
# =========================================================

class ResearchAgent:
    def __init__(self, mcp):
        self.mcp = mcp

    def run(self, query):
        print("\n--- RESEARCH AGENT ---")
        print(f"Task: {query}")

        result = self.mcp.execute(
            "Knowledge",
            query
        )

        print(f"Output: {result}")
        return result


# =========================================================
# 🤖 AGENT 2 → MATH AGENT
# =========================================================

class MathAgent:
    def __init__(self, mcp):
        self.mcp = mcp

    def run(self, expression):
        print("\n--- MATH AGENT ---")
        print(f"Task: {expression}")

        result = self.mcp.execute(
            "Calculator",
            expression
        )

        print(f"Output: {result}")
        return result


# =========================================================
# 🤖 AGENT 3 → SUMMARIZER AGENT
# =========================================================

class SummarizerAgent:
    def __init__(self, llm):
        self.llm = llm

    def run(self, user_input, research_result, math_result):
        print("\n--- SUMMARIZER AGENT ---")

        prompt = f"""
User asked:
{user_input}

Research Output:
{research_result}

Math Output:
{math_result}

Create a short final answer.

IMPORTANT:
- Include the math result clearly
- Do NOT ignore calculations
- Keep it short and clean
"""

        result = self.llm.predict(prompt)

        print(f"Final Summary: {result}")
        return result


# =========================================================
# 👑 COORDINATOR AGENT (Dynamic)
# =========================================================

class CoordinatorAgent:
    def __init__(self, llm, mcp, memory):
        self.llm = llm
        self.mcp = mcp
        self.memory = memory

        self.research_agent = ResearchAgent(mcp)
        self.math_agent = MathAgent(mcp)
        self.summarizer_agent = SummarizerAgent(llm)

    def decide_tasks(self, user_input):
        """
        LLM decides:
        1. Research question
        2. Math expression
        """

        prompt = f"""
You are a Coordinator Agent.

User Input:
{user_input}

Your job:
1. Identify the knowledge/research question
2. Identify the math calculation expression

Return ONLY valid JSON in this exact format:

{{
    "research_query": "question for research agent",
    "math_expression": "math expression only"
}}

Example:

User Input:
What is MCP and calculate 5 + 3

Output:
{{
    "research_query": "Explain Model Context Protocol (MCP)",
    "math_expression": "5 + 3"
}}
"""

        response = self.llm.predict(prompt)

        print("\n--- COORDINATOR RAW RESPONSE ---")
        print(response)

        try:
            decision = json.loads(response)
            return decision
        except Exception:
            print("⚠️ JSON parsing failed → fallback mode")
            return {
                "research_query": user_input,
                "math_expression": ""
            }

    def run(self, user_input):
        print("\n===================================")
        print("USER INPUT:")
        print(user_input)
        print("===================================")

        # ---------------------------------
        # Step 1 → Coordinator decides tasks
        # ---------------------------------

        decision = self.decide_tasks(user_input)

        research_query = decision.get(
            "research_query",
            user_input
        )

        math_expression = decision.get(
            "math_expression",
            ""
        )

        print("\n--- COORDINATOR DECISION ---")
        print(f"Research Query: {research_query}")
        print(f"Math Expression: {math_expression}")

        # ---------------------------------
        # Step 2 → Research Agent
        # ---------------------------------

        research_result = self.research_agent.run(
            research_query
        )

        # ---------------------------------
        # Step 3 → Math Agent
        # ---------------------------------

        if math_expression.strip():
            math_result = self.math_agent.run(
                math_expression
            )
        else:
            math_result = "No math calculation needed"

        # ---------------------------------
        # Step 4 → Summarizer Agent
        # ---------------------------------

        final_response = self.summarizer_agent.run(
            user_input,
            research_result,
            math_result
        )

        # ---------------------------------
        # Step 5 → Save Memory
        # ---------------------------------

        self.memory.append({
            "user_input": user_input,
            "research_query": research_query,
            "math_expression": math_expression,
            "research_output": research_result,
            "math_output": math_result,
            "final_output": final_response
        })

        save_memory(self.memory)

        return final_response


# =========================================================
# ⚙️ SYSTEM SETUP
# =========================================================

# Load memory
memory_data = load_memory()

# Create Tool Registry
registry = MCPToolRegistry()

# Register Tools
registry.register(
    "Calculator",
    calculator,
    "Math calculation tool"
)

registry.register(
    "Knowledge",
    knowledge,
    "General knowledge tool"
)

# Create MCP Executor
mcp = MCPExecutor(registry)

# Create Coordinator Agent
coordinator = CoordinatorAgent(
    llm,
    mcp,
    memory_data
)


# =========================================================
# 🚀 RUN
# =========================================================

if __name__ == "__main__":

    while True:
        user_input = input("\nYou: ")

        if user_input.lower() in ["exit", "quit"]:
            print("Exiting Multi-Agent System...")
            break

        response = coordinator.run(user_input)

        print("\n===================================")
        print("FINAL AI RESPONSE:")
        print(response)
        print("===================================")