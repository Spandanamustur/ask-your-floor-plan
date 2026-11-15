
from local_assistant import answer_question

questions = [
    "How many doors are in loopnet3?",
    "How many offices are in floorplan?",
    "How many windows are in loopnet3?",
    "How many rooms are in 19735244?",
    "Compare doors in loopnet3 and floorplan"
]

for question in questions:
    print("\nQuestion:", question)

    answer, query, parameters = answer_question(question)

    print("Answer:", answer)

    if query:
        print("SQL Query:")
        print(query)
        print("Parameters:", parameters)
