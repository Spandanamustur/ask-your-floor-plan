
import json
import csv
from pathlib import Path
from collections import Counter

DATASET_FOLDER = Path(
    r"C:\Users\Acharya\Downloads\archive\FP_annotation for sell"
)

OUTPUT_FOLDER = Path("data")
OUTPUT_FOLDER.mkdir(exist_ok=True)

def calculate_polygon_area(points):
    """Calculate polygon area using the Shoelace formula."""
    if len(points) < 3:
        return 0.0

    total = 0.0
    for i in range(len(points)):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % len(points)]
        total += x1 * y2 - x2 * y1

    return abs(total) / 2


def get_polygon_center(points):
    """Calculate the average of polygon vertex coordinates."""
    if not points:
        return None, None

    center_x = sum(point[0] for point in points) / len(points)
    center_y = sum(point[1] for point in points) / len(points)

    return center_x, center_y


all_objects = []

json_files = sorted(DATASET_FOLDER.glob("*.json"))

for json_file in json_files:
    print(f"\nProcessing: {json_file.name}")

    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    shapes = data.get("shapes", [])

    for index, shape in enumerate(shapes, start=1):
        label = shape.get("label", "unknown")
        points = shape.get("points", [])

        if shape.get("shape_type") != "polygon":
            print(f"Skipping unsupported shape: {label}")
            continue

        if len(points) < 3:
            print(f"Skipping invalid polygon: {label}")
            continue

        area = calculate_polygon_area(points)
        center_x, center_y = get_polygon_center(points)

        xs = [point[0] for point in points]
        ys = [point[1] for point in points]

        record = {
            "floorplan": json_file.stem,
            "object_id": index,
            "label": label,
            "area_pixels": round(area, 2),
            "center_x": round(center_x, 2),
            "center_y": round(center_y, 2),
            "min_x": round(min(xs), 2),
            "min_y": round(min(ys), 2),
            "max_x": round(max(xs), 2),
            "max_y": round(max(ys), 2),
            "point_count": len(points),
            "image_width": data.get("imageWidth"),
            "image_height": data.get("imageHeight")
        }

        all_objects.append(record)

    print("Objects extracted:", len(shapes))

output_file = OUTPUT_FOLDER / "floorplan_objects.csv"

if all_objects:
    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=all_objects[0].keys()
        )
        writer.writeheader()
        writer.writerows(all_objects)

print("\n===== EXTRACTION SUMMARY =====")
print("Floor plans processed:", len(json_files))
print("Total extracted objects:", len(all_objects))

label_counts = Counter(
    item["label"] for item in all_objects
)

print("\nObject counts by label:")
for label, count in sorted(label_counts.items()):
    print(f"{label}: {count}")

print("\nCSV saved to:", output_file.resolve())
