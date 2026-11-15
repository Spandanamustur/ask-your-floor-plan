
import sqlite3
import re
from pathlib import Path

DATABASE_PATH = Path("database/floorplans.db")

ROOM_LABELS = (
    "office", "open_office", "living_room", "bed_room",
    "bathroom", "rest_room", "kitchen", "kitchen_room",
    "conference_room", "meeting_room", "break_room",
    "lobby", "hall_room", "corridor", "storage_room",
    "file_room", "coffee_area", "atrium", "workspace",
    "open_area", "reception", "dining_room",
    "service_area", "mechanical_room"
)

OBJECT_TYPES = {
    "doors": "door",
    "door": "door",
    "windows": "window",
    "window": "window",
    "walls": "wall",
    "wall": "wall",
    "offices": "office",
    "office": "office",
    "bathrooms": "bathroom",
    "bathroom": "bathroom",
    "toilets": "rest_room",
    "kitchens": "kitchen",
    "kitchen": "kitchen",
    "corridors": "corridor",
    "corridor": "corridor",
}

# Related labels are suggestions only, not assumed equivalents.
RELATED_LABELS = {
    "corridor": ["hall_room", "lobby", "open_area"],
    "office": ["workspace", "open_office"],
    "bathroom": ["rest_room"],
    "kitchen": ["kitchen_room", "break_room"],
    "conference_room": ["meeting_room"],
    "storage_room": ["file_room"],
}


def get_connection():
    if not DATABASE_PATH.exists():
        raise FileNotFoundError("Floor-plan database not found.")
    return sqlite3.connect(DATABASE_PATH)


def get_floorplans():
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT floorplan_name FROM floorplans ORDER BY floorplan_name"
        )
        return [row[0] for row in cursor.fetchall()]


def find_plan_in_question(question):
    plans = get_floorplans()
    question_lower = question.lower()

    for plan in sorted(plans, key=len, reverse=True):
        if plan.lower() in question_lower:
            return plan

    return None


def count_objects(plan_name, object_type):
    query = """
        SELECT COUNT(*)
        FROM objects o
        JOIN floorplans f ON o.floorplan_id = f.id
        WHERE f.floorplan_name = ?
        AND o.label = ?
    """

    parameters = (plan_name, object_type)

    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(query, parameters)
        count = cursor.fetchone()[0]

    return count, query, parameters


def get_label_counts(plan_name, labels):
    placeholders = ",".join("?" for _ in labels)

    query = f"""
        SELECT o.label, COUNT(*)
        FROM objects o
        JOIN floorplans f ON o.floorplan_id = f.id
        WHERE f.floorplan_name = ?
        AND o.label IN ({placeholders})
        GROUP BY o.label
        ORDER BY o.label
    """

    parameters = (plan_name, *labels)

    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(query, parameters)
        results = cursor.fetchall()

    return results, query, parameters


def count_rooms(plan_name):
    placeholders = ",".join("?" for _ in ROOM_LABELS)

    query = f"""
        SELECT COUNT(*)
        FROM objects o
        JOIN floorplans f ON o.floorplan_id = f.id
        WHERE f.floorplan_name = ?
        AND o.label IN ({placeholders})
    """

    parameters = (plan_name, *ROOM_LABELS)

    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(query, parameters)
        count = cursor.fetchone()[0]

    return count, query, parameters


def list_rooms(plan_name):
    results, query, parameters = get_label_counts(
        plan_name, ROOM_LABELS
    )

    if not results:
        answer = f"No room-like spaces are annotated in {plan_name}."
    else:
        details = ", ".join(
            f"{label.replace('_', ' ')}: {count}"
            for label, count in results
        )
        answer = (
            f"Annotated room-like spaces in {plan_name}: {details}."
        )

    return answer, query, parameters


def compare_plans(question, object_type):
    plans = get_floorplans()

    mentioned = [
        plan for plan in plans
        if plan.lower() in question.lower()
    ]

    mentioned = sorted(mentioned, key=len, reverse=True)

    selected = []
    for plan in mentioned:
        if plan not in selected:
            selected.append(plan)

    if len(selected) < 2:
        return (
            "Please mention two floor-plan names to compare.",
            None,
            None
        )

    selected = selected[:2]

    query = """
        SELECT f.floorplan_name, COUNT(o.id)
        FROM floorplans f
        LEFT JOIN objects o
            ON o.floorplan_id = f.id AND o.label = ?
        WHERE f.floorplan_name IN (?, ?)
        GROUP BY f.id, f.floorplan_name
    """

    parameters = (object_type, selected[0], selected[1])

    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(query, parameters)
        results = cursor.fetchall()

    if len(results) != 2:
        return "I could not find both floor plans.", query, parameters

    answer = (
        f"{results[0][0]} has {results[0][1]} annotated "
        f"{object_type} objects. "
        f"{results[1][0]} has {results[1][1]} annotated "
        f"{object_type} objects."
    )

    return answer, query, parameters


def count_object_answer(plan_name, object_type):
    count, query, parameters = count_objects(plan_name, object_type)

    if count > 0:
        answer = (
            f"{plan_name} has {count} annotated "
            f"{object_type} objects."
        )
        return answer, query, parameters

    related_labels = RELATED_LABELS.get(object_type, [])

    if not related_labels:
        answer = (
            f"No objects labelled '{object_type}' were found "
            f"in {plan_name}."
        )
        return answer, query, parameters

    results, suggestion_query, suggestion_parameters = (
        get_label_counts(plan_name, related_labels)
    )

    if results:
        suggestions = ", ".join(
            f"{label}: {number}"
            for label, number in results
        )

        answer = (
            f"No objects are labelled '{object_type}' in "
            f"{plan_name}. However, this plan contains "
            f"{suggestions}. These are different annotation "
            f"labels, so I cannot confirm that they represent "
            f"'{object_type}'."
        )

        return answer, suggestion_query, suggestion_parameters

    answer = (
        f"No objects labelled '{object_type}' or its configured "
        f"related labels were found in {plan_name}."
    )

    return answer, query, parameters


def answer_question(question, selected_plan=None):
    question_lower = question.lower().strip()

    if not question_lower:
        return "Please enter a question.", None, None

    object_type = None

    for word, label in sorted(
        OBJECT_TYPES.items(),
        key=lambda item: len(item[0]),
        reverse=True
    ):
        if re.search(
            r"\b" + re.escape(word) + r"\b",
            question_lower
        ):
            object_type = label
            break

    if "compare" in question_lower and object_type:
        return compare_plans(question, object_type)

    plan_name = find_plan_in_question(question)

    if plan_name is None:
        plan_name = selected_plan

    if plan_name is None:
        return (
            "Please mention a floor-plan name or select one in the app.",
            None,
            None
        )

    if "list" in question_lower and any(
        word in question_lower
        for word in ["room", "space", "area"]
    ):
        return list_rooms(plan_name)

    if (
        "what rooms" in question_lower
        or "which rooms" in question_lower
    ):
        return list_rooms(plan_name)

    if "room" in question_lower and object_type is None:
        count, query, parameters = count_rooms(plan_name)

        return (
            f"{plan_name} has {count} annotated room-like spaces.",
            query,
            parameters
        )

    if object_type:
        return count_object_answer(plan_name, object_type)

    return (
        "I cannot answer this question from the supported "
        "database queries. Try asking about rooms, offices, "
        "doors, windows, walls, bathrooms, kitchens, or corridors.",
        None,
        None
    )


def debug_labels(plan_name):
    query = """
        SELECT o.label, COUNT(*)
        FROM objects o
        JOIN floorplans f ON o.floorplan_id = f.id
        WHERE f.floorplan_name = ?
        GROUP BY o.label
        ORDER BY o.label
    """

    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(query, (plan_name,))
        return cursor.fetchall()
