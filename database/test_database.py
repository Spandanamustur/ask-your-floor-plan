
import sqlite3

connection = sqlite3.connect("database/floorplans.db")
cursor = connection.cursor()

print("===== DATABASE TEST =====")

# List floor plans.
cursor.execute("""
SELECT floorplan_name, image_width, image_height
FROM floorplans
""")

print("\nFloor plans:")
for row in cursor.fetchall():
    print(row)

# Count objects by label.
cursor.execute("""
SELECT label, COUNT(*)
FROM objects
GROUP BY label
ORDER BY COUNT(*) DESC
""")

print("\nObjects by category:")
for row in cursor.fetchall():
    print(row)

# Count rooms in each floor plan.
room_labels = (
    "office", "open_office", "living_room", "bed_room",
    "bathroom", "rest_room", "kitchen", "kitchen_room",
    "conference_room", "meeting_room", "break_room",
    "lobby", "hall_room", "corridor", "storage_room",
    "file_room", "coffee_area", "atrium", "workspace",
    "open_area", "reception", "dining_room",
    "service_area", "mechanical_room"
)

placeholders = ",".join("?" for _ in room_labels)

cursor.execute(f"""
SELECT f.floorplan_name, COUNT(*)
FROM objects o
JOIN floorplans f ON o.floorplan_id = f.id
WHERE o.label IN ({placeholders})
GROUP BY f.floorplan_name
ORDER BY f.floorplan_name
""", room_labels)

print("\nRoom-like objects per floor plan:")
for row in cursor.fetchall():
    print(row)

connection.close()
print("\nDatabase test completed.")
