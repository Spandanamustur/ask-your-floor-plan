
import csv
from pathlib import Path
from collections import Counter

INPUT_FILE = Path("data/floorplan_objects.csv")
OUTPUT_FILE = Path("data/floorplan_rooms.csv")
SUMMARY_FILE = Path("data/floorplan_summary.csv")

# Labels representing spaces or rooms.
ROOM_LABELS = {
    "office",
    "open_office",
    "living_room",
    "bed_room",
    "bathroom",
    "rest_room",
    "kitchen",
    "kitchen_room",
    "conference_room",
    "meeting_room",
    "break_room",
    "lobby",
    "hall_room",
    "corridor",
    "storage_room",
    "file_room",
    "coffee_area",
    "atrium",
    "workspace",
    "open_area",
    "reception",
    "dining_room",
    "service_area",
    "mechanical_room"
}

with open(INPUT_FILE, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    objects = list(reader)

rooms = [
    item for item in objects
    if item["label"].lower() in ROOM_LABELS
]

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=rooms[0].keys())
    writer.writeheader()
    writer.writerows(rooms)

# Create a summary for each floor plan.
summary = {}

for room in rooms:
    plan = room["floorplan"]
    label = room["label"]

    if plan not in summary:
        summary[plan] = Counter()

    summary[plan][label] += 1

with open(SUMMARY_FILE, "w", newline="", encoding="utf-8") as file:
    fieldnames = ["floorplan", "total_rooms", "room_types"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()

    for plan, counts in sorted(summary.items()):
        writer.writerow({
            "floorplan": plan,
            "total_rooms": sum(counts.values()),
            "room_types": dict(counts)
        })

print("===== ROOM EXTRACTION SUMMARY =====")
print("Total annotated objects:", len(objects))
print("Room-like objects:", len(rooms))
print("Other objects:", len(objects) - len(rooms))

print("\nRoom counts by type:")
room_counts = Counter(room["label"] for room in rooms)

for label, count in sorted(room_counts.items()):
    print(f"{label}: {count}")

print("\nFiles created:")
print(OUTPUT_FILE.resolve())
print(SUMMARY_FILE.resolve())
