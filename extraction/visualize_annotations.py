
import json
import cv2
import matplotlib.pyplot as plt
from pathlib import Path


folder = Path(
    r"C:\Users\Acharya\Downloads\archive\FP_annotation for sell"
)

json_path = folder / "floorplan.json"
image_path = folder / "floorplan.jpg"


with open(json_path, "r", encoding="utf-8") as file:
    data = json.load(file)

image = cv2.imread(str(image_path))

if image is None:
    raise FileNotFoundError("Original image not found")

image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


for shape in data["shapes"]:

    label = shape["label"]
    points = shape["points"]


    polygon = [
        [int(x), int(y)]
        for x, y in points
    ]

    polygon = __import__("numpy").array(
        polygon, dtype="int32"
    )

    cv2.polylines(
        image,
        [polygon],
        True,
        (255, 0, 0),
        2
    )


plt.figure(figsize=(12, 10))
plt.imshow(image)
plt.title("Floor Plan with Polygon Annotations")
plt.axis("off")
plt.show()
