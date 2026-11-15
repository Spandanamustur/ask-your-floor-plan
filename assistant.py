
import sqlite3

DATABASE_PATH = "database/floorplans.db"

ROOM_LABELS = (
    "office", "open_office", "living_room", "bed_room",
    "bathroom", "rest_room", "kitchen", "kitchen_room",
    "conference_room", "meeting_room", "break_room",
    "lobby", "hall_room", "corridor", "storage_room",
    "file_room", "coffee_area", "atrium", "workspace",
    "open_area", "reception", "dining_room",
    "service_area", "mechanical_room"
)

def get_connection():
    return sqlite3.connect(DATABASE_PATH)


def show_floorplans():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT floorplan_name
        FROM floorplans
        ORDER BY floorplan_name
    """)

    plans = cursor.fetchall()
    connection.close()

    print("\nAvailable floor plans:")
    for plan in plans:
        print("-", plan[0])


def count_rooms(plan_name, room_type=None):
    connection = get_connection()
    cursor = connection.cursor()

    placeholders = ",".join("?" for _ in ROOM_LABELS)

    query = f"""
        SELECT COUNT(*)
        FROM objects o
        JOIN floorplans f ON o.floorplan_id = f.id
        WHERE f.floorplan_name = ?
        AND o.label IN ({placeholders})
    """

    parameters = [plan_name, *ROOM_LABELS]

    if room_type:
        query += " AND o.label = ?"
        parameters.append(room_type)

    print("\nSQL QUERY:")
    print(query)
    print("PARAMETERS:", parameters)

    cursor.execute(query, parameters)
    result = cursor.fetchone()[0]

    connection.close()
    return result


def count_objects(plan_name, object_type):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT COUNT(*)
        FROM objects o
        JOIN floorplans f ON o.floorplan_id = f.id
        WHERE f.floorplan_name = ?
        AND o.label = ?
    """

    parameters = (plan_name, object_type)

    print("\nSQL QUERY:")
    print(query)
    print("PARAMETERS:", parameters)

    cursor.execute(query, parameters)
    result = cursor.fetchone()[0]

    connection.close()
    return result



def answer_question(question):
    question_lower = question.lower().strip()

    connection = get_connection()
    cursor = connection.cursor()

    # Find a floor-plan name mentioned in the question.
    cursor.execute("""
        SELECT floorplan_name
        FROM floorplans
        ORDER BY LENGTH(floorplan_name) DESC
    """)

    available_plans = [
        row[0] for row in cursor.fetchall()
    ]

    connection.close()

    matched_plan = None

    for plan in available_plans:
        if plan.lower() in question_lower:
            matched_plan = plan
            break

    if not matched_plan:
        return (
            "I could not identify a floor plan. "
            "Please include its exact filename."
        )

    # Identify the requested object.
    if "how many rooms" in question_lower:
        result = count_rooms(matched_plan)
        return f"This floor plan has {result} annotated room-like spaces."

    if "how many offices" in question_lower:
        result = count_rooms(matched_plan, "office")
        return f"This floor plan has {result} annotated offices."

    if "how many doors" in question_lower:
        result = count_objects(matched_plan, "door")
        return f"This floor plan has {result} annotated doors."

    if "how many windows" in question_lower:
        result = count_objects(matched_plan, "window")
        return f"This floor plan has {result} annotated windows."

    if "how many walls" in question_lower:
        result = count_objects(matched_plan, "wall")
        return f"This floor plan has {result} annotated walls."

    return (
        "I cannot answer that question yet. "
        "Try asking about rooms, offices, doors, windows, or walls."
    )

if __name__ == "__main__":
    print("===================================")
    print(" ASK YOUR FLOOR PLAN")
    print("===================================")

    show_floorplans()

    print("\nAsk a question using a floor-plan filename.")
    print("Example: How many doors in floorplan?")
    print("Type 'exit' to quit.")

    while True:
        question = input("\nYour question: ")

        if question.lower().strip() == "exit":
            print("Goodbye!")
            break

        print("\nAssistant:", answer_question(question))
