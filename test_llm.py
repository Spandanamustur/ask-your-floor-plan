
from llm_assistant import ask_llm

question = "How many doors are in this floor plan?"

database_information = (
    "The selected floor plan is loopnet3. "
    "It contains 41 annotated doors."
)

print("Connecting to OpenAI...")

answer = ask_llm(
    question,
    database_information
)

print("\nAssistant Answer:")
print(answer)
