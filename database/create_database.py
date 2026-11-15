
import csv
import sqlite3
from pathlib import Path

DATA_FOLDER = Path("data")
DATABASE_FOLDER = Path("database")
DATABASE_FOLDER.mkdir(exist_ok=True)

DB_PATH = DATABASE_FOLDER / "floorplans.db"

connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

# Create floor plans table.
cursor.execute("""
CREATE TABLE IF NOT EXISTS floorplans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    floorplan_name TEXT UNIQUE,
    image_width INTEGER,
    image_height INTEGER
)
""")

# Create objects table.
cursor.execute("""
CREATE TABLE IF NOT EXISTS objects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    floorplan_id INTEGER,
    object_id INTEGER,
    label TEXT,
    area_pixels REAL,
    center_x REAL,
    center_y REAL,
    min_x REAL,
    min_y REAL,
    max_x REAL,
    max_y REAL,
    point_count INTEGER,
    FOREIGN KEY (floorplan_id) REFERENCES floorplans(id)
)
""")

# Enable foreign key enforcement.
cursor.execute("PRAGMA foreign_keys = ON")

# Import all annotated objects.
objects_file = DATA_FOLDER / "floorplan_objects.csv"

with open(objects_file, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for item in reader:
        plan_name = item["floorplan"]

        cursor.execute("""
        INSERT OR IGNORE INTO floorplans
        (floorplan_name, image_width, image_height)
        VALUES (?, ?, ?)
        """, (
            plan_name,
            int(item["image_width"]),
            int(item["image_height"])
        ))

        cursor.execute(
            "SELECT id FROM floorplans WHERE floorplan_name = ?",
            (plan_name,)
        )

        floorplan_id = cursor.fetchone()[0]

        cursor.execute("""
        INSERT INTO objects (
            floorplan_id, object_id, label, area_pixels,
            center_x, center_y, min_x, min_y,
            max_x, max_y, point_count
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            floorplan_id,
            int(item["object_id"]),
            item["label"],
            float(item["area_pixels"]),
            float(item["center_x"]),
            float(item["center_y"]),
            float(item["min_x"]),
            float(item["min_y"]),
            float(item["max_x"]),
            float(item["max_y"]),
            int(item["point_count"])
        ))

connection.commit()

# Check database contents.
cursor.execute("SELECT COUNT(*) FROM floorplans")
plan_count = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM objects")
object_count = cursor.fetchone()[0]

print("===== DATABASE CREATED =====")
print("Floor plans:", plan_count)
print("Objects:", object_count)
print("Database location:", DB_PATH.resolve())

connection.close()
