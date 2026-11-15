
import json
from pathlib import Path

file_path = Path(
    r"C:\Users\Acharya\Downloads\archive\FP_annotation for sell\floorplan.json"
)


with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

shapes = data["shapes"]

print("TOTAL OBJECTS:", len(shapes))


for shape in shapes[:5]:

    label = shape["label"]
    points = shape["points"]

    
    x_values = [point[0] for point in points]
    y_values = [point[1] for point in points]


    min_x = min(x_values)
    max_x = max(x_values)

    min_y = min(y_values)
    max_y = max(y_values)

    width = max_x - min_x
    height = max_y - min_y

    print("\nObject:", label)
    print("Number of points:", len(points))
    print("Minimum X:", min_x)
    print("Maximum X:", max_x)
    print("Minimum Y:", min_y)
    print("Maximum Y:", max_y)
    print("Width:", width)
    print("Height:", height)
