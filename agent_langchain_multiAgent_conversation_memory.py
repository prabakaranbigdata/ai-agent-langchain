from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory

# Tools
def calculator(expression):
    return str(eval(expression))

def knowledge(query):
    return llm.predict(query)

tools = [
    Tool(name="Calculator", func=calculator, description="Math calculations"),
    Tool(name="Knowledge", func=knowledge, description="General questions")
]

# LLM
llm = ChatOpenAI(
    model_name="gpt-4o-mini",
    temperature=0
)

# ✅ FIXED MEMORY
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

# ✅ FIXED AGENT TYPE
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True
)

# Test
print(agent.run("My name is Prabakaran"))
print(agent.run("What is my name?"))