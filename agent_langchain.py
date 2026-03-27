from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.tools import Tool

# Tool
def calculator(expression):
    """Use this tool to solve math expressions."""
    return str(eval(expression))

tools = [
    Tool(
        name="Calculator",
        func=calculator,
        description="Useful for math calculations"
    )
]

#  Chat Model (Correct)
llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0
)

# Agent
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Run
response = agent.run("What is 45 + 3?")
print(response)