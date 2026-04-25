from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.tools import Tool

# -------------------------------
# LLM
# -------------------------------
llm_fail = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
llm_fix = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.3)

# -------------------------------
#  FAIL VERSION (BROKEN AGENT)
# -------------------------------

def bad_calculator(expr):
    try:
        return str(eval(expr))
    except:
        return "error"

def bad_knowledge(q):
    #  Causes hallucination
    return llm_fail.predict(q)

bad_tools = [
    Tool(
        name="Calculator",
        func=bad_calculator,
        description="Can be used sometimes"
    ),
    Tool(
        name="Knowledge",
        func=bad_knowledge,
        description="General purpose tool"
    )
]

bad_agent = initialize_agent(
    bad_tools,
    llm_fail,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# -------------------------------
#  FIX VERSION (ENGINEER AGENT)
# -------------------------------

def good_calculator(expr):
    try:
        return str(eval(expr))
    except:
        return "Calculation error"

def good_knowledge(q):
    #  Safe response (no hallucination)
    return "I do not have real-time data. Please use a live API."

# good_tools = [
#     Tool(
#         name="Calculator",
#         func=good_calculator,
#         description="""
# Use ONLY for math calculations.
# Input must be a valid expression like 25*40.
# """
#     ),
#     Tool(
#         name="Knowledge",
#         func=good_knowledge,
#         description="""
# Use for general knowledge.
# Do NOT use for math.
# """
#     )
# ]

prefix = """
You are an AI agent behaving like an engineer.

Rules:
1. ALWAYS use Calculator for math.
2. NEVER calculate on your own.
3. Break problems into steps.
4. If data is real-time or unknown, say you don’t know.
"""

# good_agent = initialize_agent(
#     good_tools,
#     llm_fix,
#     agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
#     verbose=True,
#     agent_kwargs={"prefix": prefix}
# )

# -------------------------------
#  TEST CASES
# -------------------------------

print("\n==============================")
print(" FAIL AGENT (BROKEN)")
print("==============================\n")

print("1. Hallucination Test:\n")
print(bad_agent.run("What is latest stock price of TCS?"))

print("\n2. Tool Misuse Test:\n")
print(bad_agent.run("What is 25 * 40?"))

print("\n3. Reasoning Failure Test:\n")
print(bad_agent.run("Add 2+4 and multiply result by 10"))

# -------------------------------

# print("\n==============================")
# print(" FIXED AGENT (ENGINEER)")
# print("==============================\n")

# print("1. Hallucination Fixed:\n")
# print(good_agent.run("What is latest stock price of TCS?"))

# print("\n2. Tool Usage Fixed:\n")
# print(good_agent.run("What is 25 * 40?"))

# print("\n3. Step-by-Step Reasoning:\n")
# print(good_agent.run("Add 2+4 and multiply result by 10"))

# print("\n==============================")
# print(" DEMO COMPLETE")
# print("==============================\n")