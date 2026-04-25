from langchain.chat_models import ChatOpenAI

# -------------------------------
# ❌ LLM (No guardrails, pure generation)
# -------------------------------
llm = ChatOpenAI(
    model_name="gpt-4o-mini",
    temperature=0.7  # higher → more confident hallucination
)

# -------------------------------
# ❌ DIRECT QUESTION (NO TOOL, NO VALIDATION)
# -------------------------------
query = "What is the latest stock price of TCS?"

print("\n---  HALLUCINATION DEMO ---\n")

response = llm.predict(query)

print("Question:", query)
print("\nAI Answer:\n")
print(response)