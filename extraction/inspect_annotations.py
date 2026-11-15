import json
from pathlib import Path
from collections import Counter

folder = Path(
    r"C:\Users\Acharya\Downloads\archive\FP_annotation for sell"
)

json_files = sorted(folder.glob("*.json"))

print("===== ANNOTATION STRUCTURE INSPECTION =====")

for json_file in json_files:
    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    shapes = data.get("shapes", [])

    print("\n====================================")
    print("FILE:", json_file.name)
    print("Top-level JSON keys:", list(data.keys()))
    print("Number of shapes:", len(shapes))

    shape_types = Counter(
        shape.get("shape_type", "not specified")
        for shape in shapes
    )

    print("Shape types:", dict(shape_types))

    labels = Counter(
        shape.get("label", "unknown")
        for shape in shapes
    )

    print("Labels:", dict(labels))

    if shapes:
        print("\nFirst shape example:")
        print(json.dumps(shapes[0], indent=4))

print("\n===== INSPECTION COMPLETE =====")