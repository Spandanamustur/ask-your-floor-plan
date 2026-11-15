
import json
from pathlib import Path

file_path = Path(
    r"C:\Users\Acharya\Downloads\archive\FP_annotation for sell\floorplan.json"
)

with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

shapes = data["shapes"]


def calculate_polygon_area(points):
    area = 0

    number_of_points = len(points)

    for i in range(number_of_points):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % number_of_points]

        area += (x1 * y2) - (x2 * y1)

    return abs(area) / 2


print("POLYGON AREA ANALYSIS")

for shape in shapes[:10]:
    label = shape["label"]
    points = shape["points"]

    area = calculate_polygon_area(points)

    print("\nObject:", label)
    print("Area:", round(area, 2), "square pixels")
