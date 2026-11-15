
import json
import cv2
from pathlib import Path
from collections import Counter
from PIL import Image

# Dataset folder
folder = Path(
    r"C:\Users\Acharya\Downloads\archive\FP_annotation for sell"
)

print("===== FLOOR PLAN VALIDATION =====")

# Find all JSON files
json_files = sorted(folder.glob("*.json"))

for json_file in json_files:

    print("\n----------------------------")
    print("Floor plan:", json_file.stem)

    # Read JSON
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Read annotations
    shapes = data.get("shapes", [])

    print("Total objects:", len(shapes))

    # Count labels
    labels = Counter(
        shape.get("label", "unknown")
        for shape in shapes
    )

    print("Labels:", dict(labels))

    # JSON dimensions
    print("JSON image width:", data.get("imageWidth"))
    print("JSON image height:", data.get("imageHeight"))

    # Find original image
    image_path = None

    for extension in [".png", ".jpg", ".jpeg"]:
        candidate = folder / (json_file.stem + extension)

        if candidate.exists():
            image_path = candidate
            break

    if image_path is None:
        print("Original image: NOT FOUND")
        continue

    # Read original image
    image = cv2.imread(str(image_path))

    # Diagnose image loading
    if image is None:

        print("\n===== IMAGE DIAGNOSTIC =====")
        print("Image path:", image_path)
        print("File exists:", image_path.exists())
        print("File size:", image_path.stat().st_size, "bytes")

        try:
            with Image.open(image_path) as img:
                print("PIL format:", img.format)
                print("PIL dimensions:", img.size)
                img.load()
                print("PIL loading: SUCCESS")

        except Exception as error:
            print("PIL loading: FAILED")
            print("Reason:", error)

        print("OpenCV loading: FAILED")
        continue

    else:
        print("OpenCV loading: SUCCESS")

    # Check dimensions
    height, width = image.shape[:2]

    print("Actual image width:", width)
    print("Actual image height:", height)

    if (width == data.get("imageWidth")
            and height == data.get("imageHeight")):
        print("Dimension check: PASSED")
    else:
        print("Dimension check: NEEDS INVESTIGATION")

print("\n===== VALIDATION FINISHED =====")
