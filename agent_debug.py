from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory
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
        json.dump(chat_history, f)

# -------------------------------
# LLM
# -------------------------------
llm = ChatOpenAI(
    model_name="gpt-4o-mini",
    temperature=0
)

# -------------------------------
# Tools
# -------------------------------
def calculator(expression):
    return str(eval(expression))

def knowledge(query):
    return llm.predict(query)

tools = [
    Tool(name="Calculator", func=calculator, description="math calculation"),
    Tool(name="Knowledge", func=knowledge, description="General questions")
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
# Agent
# -------------------------------
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True
)

# -------------------------------
# Run + Save Memory
# -------------------------------
#response1 = agent.run("My name is Prabakaran")
#print(response1)

#response2 = agent.run("What is my name?")
#print(response2)
response1 = agent.run("What is latest stock price of TCS?")
print(response1)


# Save updated memory
chat_history = []
for msg in memory.chat_memory.messages:
    role = "human" if msg.type == "human" else "ai"
    chat_history.append({
        "type": role,
        "content": msg.content
    })

save_memory(chat_history)