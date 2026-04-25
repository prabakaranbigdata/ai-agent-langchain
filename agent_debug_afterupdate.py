from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory
from langchain.prompts import MessagesPlaceholder
from langchain.schema import SystemMessage
import json
import os

# -------------------------------
# 🧠 Long-Term Memory File
# -------------------------------
MEMORY_FILE = "memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return []

def save_memory(chat_history):
    with open(MEMORY_FILE, "w") as f:
        json.dump(chat_history, f, indent=2)

# -------------------------------
# LLM
# -------------------------------
llm = ChatOpenAI(
    model_name="gpt-4o-mini",
    temperature=0.3
)

# -------------------------------
# Tools
# -------------------------------
def calculator(expression):
    try:
        return str(eval(expression))
    except Exception:
        return "Error in calculation"

def knowledge(query):
    return llm.predict(query)

tools = [
    Tool(
        name="Calculator",
        func=calculator,
        description="Use this tool for ALL math calculations. Return only the result. Do NOT explain."
    ),
    Tool(
        name="Knowledge",
        func=knowledge,
        description="Use this tool for general knowledge questions."
    )
]

# -------------------------------
# 🧠 Load Long-Term Memory
# -------------------------------
stored_messages = load_memory()

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

# Restore previous messages
for msg in stored_messages:
    if msg["type"] == "human":
        memory.chat_memory.add_user_message(msg["content"])
    else:
        memory.chat_memory.add_ai_message(msg["content"])

# -------------------------------
# 🔥 Strong Debug Prompt
# -------------------------------
system_message = SystemMessage(content="""
You are an AI agent behaving like an engineer.

STRICT PROCESS:
1. Identify tasks separately
2. Use Calculator for math
3. Use Knowledge tool for info
4. Execute step-by-step

Output:
Step 1: Task breakdown
Step 2: Tool usage
Step 3: Final answer
""")
# system_message = SystemMessage(content="""
# You are a helpful assistant.
# Answer user queries.
# """)

# -------------------------------
# Agent
# -------------------------------
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True,
    agent_kwargs={
        "system_message": system_message,
        "extra_prompt_messages": [MessagesPlaceholder(variable_name="chat_history")]
    }
)

# -------------------------------
# 🧪 Demo Input
# -------------------------------
print("\n--- Running Improved Agent ---\n")

response = agent.run("Tell me about Python and addition of two numbers 2,4")
print("\nFinal Answer:\n")
print(response)

# -------------------------------
# 💾 Save Updated Memory
# -------------------------------
chat_history = []
for msg in memory.chat_memory.messages:
    role = "human" if msg.type == "human" else "ai"
    chat_history.append({
        "type": role,
        "content": msg.content
    })

save_memory(chat_history)

print("\nMemory saved to memory.json\n")