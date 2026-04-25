from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

prompt = """
Create a JSON output with the following fields:
name, role, skills, experience.

Input:
Software engineer named Ravi with Python and AI skills.He have experience in Building applications
"""

response = llm.predict(prompt)

print("\n✅ STRUCTURED OUTPUT:\n")
print(response)