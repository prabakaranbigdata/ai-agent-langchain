from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

response = llm.predict(
    "Create a profile for a software engineer named Ravi with Python and AI skills. He have experience in Building applications"
)

print("\n UNSTRUCTURED OUTPUT:\n")
print(response)