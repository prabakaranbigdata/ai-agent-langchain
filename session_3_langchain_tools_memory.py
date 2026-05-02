# =========================================================
# LANGCHAIN STABLE VERSION (TOOLS + MEMORY)
# =========================================================

from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory
import warnings
warnings.filterwarnings("ignore")

# =========================================================
# 🧠 LLM
# =========================================================

llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

# =========================================================
# 🔧 TOOLS
# =========================================================

def travel_info_func(_):
    return "Train:1500, Stay:1000/night, Food:500/day, Scooter:400/day"

def calculator_func(expression):
    try:
        return str(eval(expression))
    except:
        return "ERROR"

tools = [
    Tool(name="TravelInfo", func=travel_info_func, description="Get travel cost"),
    Tool(name="Calculator", func=calculator_func, description="Do math calculation")
]

# =========================================================
# 🧠 MEMORY
# =========================================================

memory = ConversationBufferMemory(memory_key="chat_history")

# =========================================================
# 🤖 AGENT
# =========================================================

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True
)

# =========================================================
# ▶️ RUN
# =========================================================

if __name__ == "__main__":
    while True:
        query = input("Enter: ")
        print(agent.run(query))