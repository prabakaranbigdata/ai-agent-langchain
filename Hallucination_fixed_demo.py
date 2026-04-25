from langchain.chat_models import ChatOpenAI

# -------------------------------
# ✅ LLM (controlled)
# -------------------------------
llm = ChatOpenAI(
    model_name="gpt-4o-mini",
    temperature=0   # reduce randomness
)

# -------------------------------
# ✅ Guardrail Function
# -------------------------------
def safe_response(query):
    """
    Prevent hallucination for real-time or unknown data
    """
    real_time_keywords = ["latest", "current", "today", "now", "stock price"]

    # Check if query needs real-time data
    if any(word in query.lower() for word in real_time_keywords):
        return "I do not have real-time data access. Please use a live API or trusted source."

    # Otherwise, allow LLM response
    return llm.predict(query)

# -------------------------------
# 🧪 TEST QUERY
# -------------------------------
query = "What is the latest stock price of TCS?"

print("\n--- ✅ HALLUCINATION FIXED ---\n")

response = safe_response(query)

print("Question:", query)
print("\nAI Answer:\n")
print(response)