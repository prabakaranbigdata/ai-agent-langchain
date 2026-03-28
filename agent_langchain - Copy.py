from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.tools import Tool

#  Tool 1: Calculator
def calculator(expression):
    """Use this tool to solve math expressions."""
    return str(eval(expression))


#  Tool 2: Knowledge (General Questions)
def knowledge(query):
    """Use this tool to answer general knowledge questions."""
    
    # Simple demo logic (you can expand later)
    if "capital of india" in query.lower():
        return "The capital of India is New Delhi."
    elif "ai agents" in query.lower():
        return "AI agents are systems that can think and act."
    else:
        return "I don't have information on that."


# 🔧 Tool List
tools = [
    Tool(
        name="Calculator",
        func=calculator,
        description="Useful for math calculations"
    ),
    Tool(
        name="Knowledge",
        func=knowledge,
        description="Useful for answering general knowledge questions"
    )
]

#  Chat Model
llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0
)

# 🤖 Agent
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

#  Run Examples
response1 = agent.run("What is 45 + 3?")
print("Math:", response1)

response2 = agent.run("What is capital of India?")
print("GK:", response2)